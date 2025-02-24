# Copyright 2020-2022 Michael Thies <mail@mhthies.de>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import asyncio
import logging
import warnings
from typing import Awaitable, Callable, List, Any, Optional, AsyncIterator

from .packets import ReceivedGroupAPDU, KNXDPacket, KNXDPacketTypes, GroupAddress, KNXDAPDUType, EncodedData, \
    KNXGroupAPDU

logger = logging.getLogger(__name__)


class KNXDConnection:
    """
    A connector for the KNXd native protocol. It wraps an asyncio TCP or UNIX socket server and provides highlevel
    (async) methods to interact with KNXd.

    The main control flow for the connector is split into three methods:

    * :meth:`connect` trys to open the TCP/unix socket to connect to KNXd. It returns upon successful estalishment of
        the connection or raises an exception.
    * :meth:`run` runs the main receive loop for incoming messages (like Group Addres telegrams). It spins in an await
        loop until the connector has been stopped gracefully. In case of a read error, an exception is raised.
    * :meth:`stop` initiates a graceful shutdown and termination of the connection.

    To send and receive Group Address packets, a Group Socket must be opened in KNXD. This is initiated by the
    :meth:`open_group_socket` method. However, this method requires the receive loop (i.e. the :meth:`run` method)
    to be already running in an second asyncio task.

    After opening the Group Socket, incoming Group Address telegrams are registered and passed on to all handler
    functions, registered via :meth:`register_telegram_handler`. To send a Group Address telegram, :meth:`group_write`
    can be used.

    In summary, a typical invocation of this connector looks like this::

        def handler(packet: knxdclient.ReceivedGroupAPDU) -> None:
            print("Received group telegram: {}".format(packet))

        connection = KNXDConnection()
        connection.set_group_apdu_handler(handler)
        await connection.connect()
        # Connection was successful. Start receive loop:
        run_task = asyncio.create_task(connection.run())
        # Now that the receive loop is running, we can open the KNXd Group Socket:
        await connection.open_group_socket()

        # Startup completed. Now our `handler()` will receive incoming telegrams and we can send some:
        await connection.group_write(GroupAddress(1,3,2), KNXDAPDUType.WRITE, encode_value(True, KNXDPT.BOOLEAN))

        # Let's stop the connection and wait for graceful termination of the receive loop:
        await connection.stop()
        await run_task

    :param timeout: Maximum time between packets received from KNXD. If the timeout is exceeded, the `run()` coroutine
                    will terminate with a TimeoutError or asyncio.TimeoutError (depending on Python version).
                    If None (default), no timeout is applied.
                    Typically, no timeout should be required, as connection failures are detected by the OS and
                    signalled by closing the network socket.
                    Make sure to only use the `timeout` parameter, if regular packets from KNXD is expected (e.g. due
                    to regular activity on the KNX bus).
    """
    def __init__(self, timeout: Optional[float] = None):
        self._group_apdu_handler: Optional[Callable[[ReceivedGroupAPDU], Any]] = None
        self.closing = False
        self._current_response: Optional[KNXDPacket] = None
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._timeout: Optional[float] = timeout
        # A lock to ensure, that only one synchronous action is performed on the KNXD connection at once. Synchronous
        # actions are for example EIB_OPEN_GROUPCON. The lock should be acquired before sending the synchronous request
        # packet to KNXD and only released after receiving the response packet from KNXD.
        # Sending and receiving group telegrams via an opened Group Socket is asynchronous and thus does not require the
        # lock.
        self._lock = asyncio.Lock()
        # An (asyncio) event to await the receipt of a synchronous response packet from KNXD. Before sending a
        # synchronous request packet to KNXD, a coroutine method should ``clear()`` this event; and afterwards
        # ``wait()`` on it. As soon as a response is received by the :meth:`run` coroutine, it will store the response
        # in ``_current_response` and inform the waiting method by setting the event.
        self._response_ready = asyncio.Event()
        # An (asyncio) event that checks whether "run" coroutine has exited or is still executing
        self._run_exited = asyncio.Event()

    async def connect(self, host: str = 'localhost', port: int = 6720, sock: Optional[str] = None):
        """
        Coroutine to connect to KNXd/EIBd via TCP port or UNIX socket

        Awaits until connection has been established or raises one of Python's built in Exceptions on connection errors.

        If a connection has already been established before, it is closed before creating a new one.

        :param host: KNXd host for TCP connection. Defaults to 'localhost'. Ignored, if `sock` is present.
        :param port: Port for KNXd TCP connection. Defaults to 6720, which is KNXd's default port. Ignored, if `sock` is
            present.
        :param sock: Path of the KNXd UNIX socket. If given, `host` and `port` are ignored.
        """
        # Close previous connection gracefully if any
        if self._writer is not None:
            # In case of a reconnect unset the _run_exited asyncio.Event
            self._run_exited.clear()
            if not self._writer.is_closing():
                self._writer.close()
            await self._writer.wait_closed()

        if sock:
            logger.info("Connecting to KNXd via UNIX domain socket at %s ...", sock)
            self._reader, self._writer = await asyncio.open_unix_connection(sock)
        else:
            logger.info("Connecting to KNXd at %s:%s ...", host, port)
            self._reader, self._writer = await asyncio.open_connection(host=host, port=port)
        logger.info("Connecting to KNXd successful")

    async def _read_raw_knxpacket(self) -> bytes:
        assert self._reader is not None
        length = int.from_bytes(await self._reader.readexactly(2), byteorder='big')
        return await self._reader.readexactly(length)

    async def run(self):
        """
        Coroutine for running the receive loop for incoming packets from EIBD/KNXD.

        This method awaits incoming packets in a loop and only returns upon successful shutdown via :meth:`stop`. In
        case of an ``ConnectionError`` or an unexpected connection termination, an exception is raised. Other
        exceptions occuring within the loop are caught and logged.

        The connection with KNXD must be opened using :meth:`connect`, before starting this coroutine.

        Incoming packets are separated by their type:
        * for each packet of type *EIB_GROUP_PACKET* (asynchronous message from KNXD), all registered telegram handlers
          are called with the payload decoded as :class:`ReceivedGroupAPDU`
        * for every other (synchronous response) EIBD packet type, the packet is stored in an internal buffer and
          waiting synchronous KNXD request functions (like :meth:`open_group_socket`) are informed.

        :raises ConnectionAbortedError: in case of an unexpected EOF (connection closed without ``stop()`` being called)
        :raises ConnectionError: in case such an error occurs while reading
        :raises ConnectionError: when no connection has been established yet or the previous connection reached an EOF.
        :raises TimeoutError: If given `timeout` is exceeded between packets received from KNXD (Python >= 3.11)
        :raises asyncio.TimeoutError: If given `timeout` is exceeded between packets received from KNXD (Python < 3.11)
        """
        if self._reader is None or self._reader.at_eof():
            raise ConnectionError("No connection to KNXD has been established yet or the previous connection's "
                                  "StreamReader is at EOF")
        logger.info("Entering KNXd client receive loop ...")
        self._run_exited.clear()

        while True:
            try:
                data = None
                if self._timeout is not None:
                    read_task = self._read_raw_knxpacket()
                    data = await asyncio.wait_for(read_task, self._timeout)
                else:
                    data = await self._read_raw_knxpacket()

                packet = KNXDPacket.decode(data)
                logger.debug("Received packet from KNXd: %s", packet)
                if packet.type is KNXDPacketTypes.EIB_GROUP_PACKET:
                    apdu = ReceivedGroupAPDU.decode(packet.data)
                    logger.debug("Received Group Address broadcast (APDU) from KNXd: %s", apdu)
                    if self._group_apdu_handler:
                        self._group_apdu_handler(apdu)
                else:
                    self._current_response = packet
                    self._response_ready.set()
            except asyncio.IncompleteReadError as e:
                self._run_exited.set()
                if self.closing:
                    logger.info("KNXd connection reached EOF. KNXd client is stopped.")
                    return
                else:
                    raise ConnectionAbortedError("KNXd connection was closed with EOF unexpectedly.") from e
            # From python 3.11 it will raise a stdlib TimeoutError instead of asyncio.TimeoutError
            except (ConnectionError, TimeoutError, asyncio.TimeoutError, asyncio.CancelledError) as error:
                # A connection, timeout or cancellation errors
                # typically mean we cannot proceed further with this connection.
                # Thus we abort the receive loop execution with the exception.
                logger.error("Error while waiting for next packet from KNXd: %s. "
                             "Exiting from receive loop.", repr(error))
                self._run_exited.set()
                raise
            except Exception as e:
                logger.error("Error while receiving KNX packets:", exc_info=e)
                self._run_exited.set()
                raise

    async def stop(self):
        """
        Coroutine to initiate a graceful shutdown of the KNXD connection.

        This coroutine awaits the successful shutdown of the connection.
        """
        if self._writer is None:
            return
        logger.info("Stopping KNXd client ...")
        self.closing = True
        self._writer.close()
        await self._writer.wait_closed()

    def set_group_apdu_handler(self, handler: Callable[[ReceivedGroupAPDU], Any]) -> None:
        """
        Set the callback handler for incoming group read/response/write telegrams.

        The :meth:`run` coroutine will call the handler function in the context of the asyncio EventLoop for
        every incoming group telegram (asynchronous message from KNXD), one after another. The handler may then dispatch
        the telegrams, spawn a Task for each one, etc. To enable receiving of group telegrams, a Group Socket has to be
        opened in KNXD.

        Only a single handler function can be registered. Either a custom handler can be registered or
        :meth:`iterate_group_telegrams` can be used, not both. To dispatch each incoming group telegram to multiple
        handler functions you need to implement a handler dispatcher yourself.

        :param handler: The callback function. It must take a single argument of type :class:`ReceivedGroupAPDU`.
        :raises RuntimerError: When another handler has been registered before or :meth:`iterate_group_telegrams` is
            already in use.
        """
        if self._group_apdu_handler:
            raise RuntimeError("Another group APDU handler has already been registered or iterate_group_telegrams() is "
                               "in use.")
        self._group_apdu_handler = handler

    async def iterate_group_telegrams(self) -> AsyncIterator[ReceivedGroupAPDU]:
        """
        Create an asynchronous iterator for iterating over group read/response/write telegrams as they are received from
        KNXD.

        The method creates an asynchronous iterator that will yield all received group telegrams as soon as they are
        received. They can be iterated using an `async for` loop. To enable receiving of group telegrams, a Group Socket
        has to be opened in KNXD::

            await knx_connection.connect()
            run_task = asyncio.create_task(knx_connection.run())
            await knx_connection.open_group_socket()
            try:
                async for telegram in knx_connection.iterate_group_telegrams():
                    print("Received telegram: ", telegram)
            finally:
                run_task.cancel()

        Only a single asynchronous iterator for receiving the group telegrams can be used at the same time. It can only
        be used alternatively, not together with a custom group apdu handler, as registered with
        :meth:`set_group_apdu_handler`.

        :raises RuntimerError: When a custom handler function has been registered or another iterator is already active
        :raises ConnectionAbortedError: in case the `run()` loop exited unexpectedly while waiting for messages
        """
        if self._group_apdu_handler:
            raise RuntimeError("A custom group APDU handler has already been registered or iterate_group_telegrams() is"
                               " already in use.")

        queue: asyncio.Queue[ReceivedGroupAPDU] = asyncio.Queue()
        self._group_apdu_handler = queue.put_nowait
        try:
            run_exited = asyncio.create_task(self._run_exited.wait())
            while True:
                try:
                    next_message_task = asyncio.create_task(queue.get())
                    done, _pending = await asyncio.wait((next_message_task, run_exited),
                                                        return_when=asyncio.FIRST_COMPLETED)

                    if run_exited in done:
                        raise ConnectionAbortedError("KNXDConnection was closed and is no longer sending messages")

                    yield next_message_task.result()
                finally:
                    next_message_task.cancel()
        except Exception as ex:
            logger.error(ex)
            raise
        finally:
            run_exited.cancel()
            self._group_apdu_handler = None

    async def open_group_socket(self, write_only=False) -> None:
        """
        Coroutine to request KNXD to open a Group Socket for sending and receiving group telegrams to/from any Group
        Address.

        This is a synchronous KNXD function, i.e. it will send a request packet to KNXD and await the receipt of a
        response packet from KNXD.
        Attention: This coroutine requires :meth:`run` to be running in a separate task of the **same** asyncio event
        loop!

        :param write_only: If True, KNXD is requested to open the Group Socket in write-only mode, i.e. no incoming
            group telegrams will be received.
        :raises RuntimeError: when KNXD responds with an error message or an unexpected response packet.
        :raises ConnectionAbortedError: in case the `run()` loop exited unexpectedly while waiting for the response
        """
        logger.info("Opening KNX group socket for sending to group addresses ...")
        async with self._lock:
            self._response_ready.clear()
            await self._send_eibd_packet(KNXDPacket(KNXDPacketTypes.EIB_OPEN_GROUPCON,
                                                    bytes([0, 0xff if write_only else 0, 0])))

            run_exited = asyncio.create_task(self._run_exited.wait())
            response_ready = asyncio.create_task(self._response_ready.wait())

            done, _pending = await asyncio.wait((run_exited, response_ready), return_when=asyncio.FIRST_COMPLETED)

            if run_exited in done:
                response_ready.cancel()
                raise ConnectionAbortedError("KNXDConnection was closed and is no longer sending messages")
            run_exited.cancel()

            response = self._current_response
        assert response is not None
        if response.type is not KNXDPacketTypes.EIB_OPEN_GROUPCON:
            raise RuntimeError("Could not open KNX group socket. Response: {}".format(response))
        else:
            logger.info("Opening KNX group socket successful")

    async def group_write(self, addr: GroupAddress, write_type: KNXDAPDUType, encoded_data: EncodedData) -> None:
        """
        Send a Group Read/Response/Write telegram to the KNX bus via a KNXD Group Socket.

        This requires an open connection to KNXD and a KNXD Group Socket being opened on this connection. See
        :meth:`connect` and :meth:`open_group_socket`.

        This coroutine awaits the sending (including flushing the write buffer) of the packet to KNXD.

        :param addr: The KNX group address as :class:`GroupAddress`
        :param write_type: The telegram type (read/response/write) as :class:`KNXDAPDUType`
        :param encoded_data: The payload data, binary encoded for KNX transmission, as returned by :func:`encode_data`
            when called with the correct KNX Datapoint type for the relevant Group Address.
        """
        logger.debug("%s to KNX group address %s: %s", write_type.name, addr, encoded_data)
        await self._send_eibd_packet(KNXDPacket(KNXDPacketTypes.EIB_GROUP_PACKET,
                                                addr.encode() + KNXGroupAPDU(write_type, encoded_data).encode()))

    async def _send_eibd_packet(self, packet: KNXDPacket) -> None:
        """
        Send a packet to KNXD via its simple TCP/UNIX protocol.

        Requires an open connection to KNXD.
        This coroutine awaits the sending (including flushing the write buffer) of the packet to KNXD.

        :param packet: The packet to send, as a :class:`KNXDPacket`
        :raises ValueError: If the encoded packet has an invalid length (< 2 or > 65535)
        :raises ConnectionError: If no connection has been established yet or the connection is closing
        """
        if self._writer is None or self._writer.is_closing():
            raise ConnectionError("No connection to KNXD has been established yet or the previous connection's "
                                  "StreamWriter is closing")
        logger.debug("Sending packet to KNXd: %s", packet)
        data = packet.encode()
        if len(data) < 2 or len(data) > 0xffff:
            raise ValueError('Invalid packet length: {}'.format(repr(data)))
        data = len(data).to_bytes(2, byteorder='big') + data
        self._writer.write(data)
        await self._writer.drain()
