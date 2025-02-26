"""
A simple network extention for simple and easy connections between different devices.
"""

import socket
import struct
import hashlib
import time
import hmac
import secrets
from collections.abc import Buffer, Iterable
from typing import TypeAlias, Any, overload, Callable, Optional
from dataclasses import dataclass
from cryptography.fernet import Fernet
from threading import Thread, Lock
from enum import Enum

# Buffers are a direct copy from '_typeshed' since their 
# unobtainable in a simple extention like this from my 
# knowledge thus far.

# Unfortunately PEP 688 does not allow us to distinguish read-only
# from writable buffers. We use these aliases for readability for now.
# Perhaps a future extension of the buffer protocol will allow us to
# distinguish these cases in the type system.
ReadOnlyBuffer: TypeAlias = Buffer  # stable
WriteableBuffer: TypeAlias = Buffer
ReadableBuffer: TypeAlias = Buffer  # stable
_Address: TypeAlias = tuple[Any, ...] | str | ReadableBuffer # Direct copy from socket reference
_RetAddress: TypeAlias = Any # Direct copy from socket reference

# Cleanup
del Buffer, TypeAlias

class HMAC_Incorrect(Exception):
    """HMAC was incorrect."""
    ...

class ChecksumError(Exception):
    """A error when calculating checksums."""
    ...

class SecureMessage:
    """A class for secure network messages."""
    def __init__(self, key: bytes = None, hmac_key: bytes = None):
        """Initialize SecureMessage with an encryption key, or generate a new one."""
        self.key = key or Fernet.generate_key()
        self.hmac_key = hmac_key or secrets.token_bytes(32)
        self.cipher = Fernet(self.key)
    
    def _generate_hmac(self, data: bytes) -> bytes:
        """Generate an HMAC signature for the given data."""
        return hmac.new(self.hmac_key, data, hashlib.sha256).digest()

    def _verify_hmac(self, data: bytes, signature: bytes) -> bool:
        """Verify the HMAC signature."""
        return hmac.compare_digest(self._generate_hmac(data), signature)

    def add_checksum(self, data: bytes) -> bytes:
        """Add a SHA256 checksum to the data."""
        checksum = hashlib.sha256(data).digest()  # 32 bytes checksum
        return checksum + data

    def verify_checksum(self, data: bytes) -> bytes:
        """Verify and remove the checksum from the data. Raises ValueError if invalid."""
        if len(data) < 32:
            raise ChecksumError("Data is too short to contain a checksum.")
        
        checksum, payload = data[:32], data[32:]
        expected_checksum = hashlib.sha256(payload).digest()
        
        if checksum != expected_checksum:
            raise ChecksumError("Checksum verification failed! Data may be corrupted.")
        
        return payload
    
    def pack(self, data: bytes) -> bytes:
        """Pack data into a format that is ready to be sent and handled by a receiver."""
        encrypted_data = self.encrypt(data)
        length_prefix = struct.pack(">I", len(encrypted_data))  # 4-byte length header
        return length_prefix + encrypted_data

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data with checksum and generate HMAC before encryption."""
        secure_data = self.add_checksum(data)  # Append checksum before encryption
        signature = self._generate_hmac(secure_data)  # Generate HMAC for plaintext
        encrypted_data = self.cipher.encrypt(secure_data)  # Encrypt
        return signature + encrypted_data  # Prepend HMAC

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Verify HMAC, then decrypt and validate checksum."""
        if len(encrypted_data) < 32:
            raise HMAC_Incorrect("Data too short for HMAC verification!")

        signature, actual_data = encrypted_data[:32], encrypted_data[32:]  # Extract HMAC
        decrypted_data = self.cipher.decrypt(actual_data)  # Decrypt data

        if not self._verify_hmac(decrypted_data, signature):
            raise HMAC_Incorrect("HMAC verification failed! Data may be tampered with.")

        return self.verify_checksum(decrypted_data)  # Validate checksum

class PacketSizeError(Exception):
    """
    The packet size recieved was unexpectedly large. 
    This error is raised for security messures.

    If you still want the data from this event, 
    you can simply extract it from the `data` attribute.
    """
    def __init__(self, *args: object, data: str):
        self.data: str = data
        super().__init__(*args)

class receiver:
    """The reciever handles receiving data."""
    MAX_PACKET_SIZE = 65536  # Example limit: 64KB

    @staticmethod
    def recv(socket: socket.socket, encryptor: SecureMessage) -> bytes:
        """Recieve data for a socket with it's encryptor."""
        length_data = receiver._recv_exact(socket, 4)  # Read the 4-byte length prefix
        if not length_data: raise ConnectionError("Connection closed before length received.")
            
        data_length = struct.unpack(">I", length_data)[0]  # Unpack big-endian 4-byte length

        # Protect against DoS by limiting max size
        if data_length > receiver.MAX_PACKET_SIZE:
            data = encryptor.decrypt(receiver._recv_exact(socket, data_length)) # Read the full encrypted payload to get rid of it
            raise PacketSizeError(f"Packet too large! {data_length} bytes exceeds {receiver.MAX_PACKET_SIZE} bytes.", data = data)

        encrypted_data = receiver._recv_exact(socket, data_length)  # Read the full encrypted payload
        return encryptor.decrypt(encrypted_data)
    
    @staticmethod
    def _recv_exact(socket: socket.socket, num_bytes: int) -> bytes:
        """Helper function to receive exactly num_bytes from the socket."""
        data = bytearray()
        while len(data) < num_bytes:
            chunk = socket.recv(num_bytes - len(data))
            if not chunk:
                raise ConnectionError(f"Connection closed early! Expected {num_bytes} bytes, got {len(data)}.")
            data.extend(chunk)
        return bytes(data)

@dataclass
class simple_socket:
    """A network connection."""
    encryptor: SecureMessage
    socket: Optional['socket.socket'] = None

    def send(self, data: ReadableBuffer, flags: int = 0, /) -> None:
        self.socket.send(self.encryptor.pack(data), flags) # NO keyword arguments, huh...

    def sendall(self, data: ReadableBuffer, flags: int = 0, /) -> None:
        self.socket.sendall(self.encryptor.pack(data), flags)
    
    def sendfile(self, file: 'socket._SendableFile', offset: int = 0, count: int | None = None) -> int:
        return self.socket.sendfile(file = file, offset = offset, count = count)
    
    @overload
    def sendto(self, data: ReadableBuffer, address: _Address, /) -> int: ...

    @overload
    def sendto(self, data: ReadableBuffer, flags: int, address: _Address, /) -> int: ...
    
    def sendto(self, data: ReadableBuffer, *args: Any) -> int:
        if len(args) == 1:  # Address only
            address = args[0]
            return self.socket.sendto(self.encryptor.pack(data), address)
        elif len(args) == 2:  # Flags and address
            flags, address = args
            return self.socket.sendto(self.encryptor.pack(data), flags, address)
        else:
            raise ValueError("Invalid arguments")
    
    def recv(self) -> bytes:
        return receiver.recv(self.socket, self.encryptor)
    
    def accept(self) -> tuple['socket.socket', _RetAddress]:
        return self.socket.accept()
    
    def detach(self) -> int:
        return self.socket.detach()
    
    def bind(self, address: 'socket._Address', /) -> None:
        self.socket.bind(address = address)
    
    def listen(self, backlog: int = 0, /) -> None:
        self.socket.listen(backlog = backlog)
    
    def close(self) -> None:
        self.socket.close()
    
    def setblocking(self, flag: bool, /) -> None:
        self.socket.setblocking(flag = flag)
    
    def settimeout(self, value: float | None, /) -> None:
        self.socket.settimeout(value = value)

    def share(self, process_id: int, /) -> bytes:
        return self.socket.share(process_id = process_id)
    
    def shutdown(self, how: int, /) -> None:
        self.socket.shutdown(how = how)

    def connect(self, address: tuple[str | None, int], timeout: float | None = None, /, *args, **kwargs) -> 'socket.socket':
        self.socket = socket.create_connection(address = address, timeout = timeout, *args, **kwargs)
        return self.socket
    
    def create(self, address: 'socket._Address', /, *args, **kwargs) -> 'socket.socket':
        self.socket = socket.create_server(address = address, *args, **kwargs)
        return self.socket
    
    @property
    def address(self) -> _RetAddress:
        return self.socket.getsockname()

class META:
    """This method represent meta data for a even type."""
    def __init__(self, id: Any, description: Optional[str]):
        self.id: Any = id
        self.description: Optional[str] = description

class EventType(Enum):
    """A event type represent a specific type of event."""
    CONNECTION_REQUEST = META("Connection request", "Someone is trying to connect")
    CONNECTION_SUCCESS = META("Connection success", "Someone has successfully connected")
    CONNECTED = META("Connected", "The client or server has connected / Started communicating")
    DISCONNECTED = META("Disconnected", "A client or server has disconnected")
    RECEIVED = META("Recieved", "Recieved data from a device")
    THREAD_WARNING = META("Thread warning", "A thread did not behave as expected")
    ERROR = META("Error", "A error has occured somewhere - self explainatory")

    @property
    def id(self):
        return self.value.id
    
    @property
    def description(self):
        return self.value.description

class Event:
    """A event. It consists of a type, data and methods."""
    def __init__(self, type: EventType, data: dict[str, Any] = {}, /, **kwargs):
        self.type: EventType = type
        self.data: dict[str, Any] = data # For data that may need to be mobile, like data or connections
        self.extra: dict[str, Any] = kwargs
        for key, item in kwargs.items(): setattr(self, key, item) # For data alike callables
    
    def __str__(self) -> str:
        return f"{self.type.id}: {self.type.description} | {self.data} | Extra: {', '.join(self.extra.keys())}"
    
    def __repr__(self) -> str:
        data_repr = repr(self.data)
        if len(data_repr) > 100:  # Limit output size
            data_repr = data_repr[:100] + "... (truncated)"
        return f"{self.__class__.__name__}(type={repr(self.type)}, data={data_repr}, {', '.join(f'{key}={repr(value)}' for key, value in self.extra.items())})"

class Server:
    """A server - it can have a network of clients of which it can share data between."""
    def __init__(self, key: bytes | None, hmac_key: bytes | None, address: _Address, on_event: Callable[[Event], Any], max_clients: Optional[int] = None):
        """Create a new server."""
        self.socket: simple_socket = simple_socket(SecureMessage(key, hmac_key))
        self.address: _Address = address
        self.threads: list[Thread] = []
        self.on_event: Callable[[Event], Any] = on_event

        self.clients: dict[_RetAddress, socket.socket] = {}
        self.clients_lock = Lock()  # Add a lock here

        self.max_clients: Optional[int] = max_clients
        self.active: bool = False
    
    def send(self, data: ReadableBuffer, flags: int = 0, /) -> None:
        """Send something to all the clients."""
        for addr, conn in self.clients.items():
            conn.sendall(self.socket.encryptor.pack(data), flags)
    
    @overload
    def sendto(self, data: ReadableBuffer, address: _RetAddress, /) -> None: ...
    
    @overload
    def sendto(self, data: ReadableBuffer, flags: int, address: _RetAddress, /) -> None: ...
    
    def sendto(self, data: ReadableBuffer, *args: Any) -> None:
        """Send to a specific address."""
        if len(args) == 1:  # Address only
            address = args[0]
            self.clients[address].sendall(self.socket.encryptor.pack(data))
        elif len(args) == 2:  # Flags and address
            flags, address = args
            self.clients[address].sendall(self.socket.encryptor.pack(data), flags)
        else:
            raise ValueError("Invalid arguments")
    
    def init(self) -> None:
        """Start listening."""
        # Start server
        self.socket.create(self.address)

        self.active = True

        # Start listener
        listen_thread = Thread(target = self._listen)
        self.threads.append(listen_thread)
        listen_thread.start()

        self.on_event(Event(EventType.CONNECTED))
    
    def _handle_client(self, addr: _RetAddress, conn: socket.socket):
        with self.clients_lock:  # Ensure thread-safe access
            self.clients[addr] = conn

        self.on_event(Event(EventType.CONNECTION_SUCCESS, 
            {"address": addr, "connection": conn}
        ))

        try:
            while self.active:
                data = receiver.recv(conn, self.socket.encryptor)
                self.on_event(Event(EventType.RECEIVED,
                    {"address": addr, "connection": conn, "data": data}
                ))
        except (ConnectionError, PacketSizeError, OSError) as e:
            self.on_event(Event(EventType.ERROR, 
                {"exception": e},
                close = self.close
            ))
        finally:
            self.clients.pop(addr, None)
            conn.close()
            del conn, addr # Remove completely - just to be sure, I suppose?
    
    def _listen(self) -> None:
        try:
            while self.active:
                conn, addr = self.socket.accept()

                thread = Thread(target = self._handle_client, args = (addr, conn,))

                accept: Callable[[], None] = lambda: (self.threads.append(thread), thread.start())
                reject: Callable[[], None] = lambda: conn.close()
                
                if not self.max_clients or len(self.clients) < self.max_clients:
                    self.on_event(Event(EventType.CONNECTION_REQUEST, 
                        {"address": addr, "connection": conn},
                        accept = accept, 
                        reject = reject
                    ))
                else: reject()
            return # Return if no errors
        except Exception as e:
            self.on_event(Event(EventType.ERROR, 
                {"exception": e},
                close = self.close
            ))
    
    def close(self) -> None:
        """Close the server."""
        self.active = False  # Stop all operations
        if not hasattr(self, "_disconnected"):  # Prevent duplicate event
            self._disconnected = True  
            self.on_event(Event(EventType.DISCONNECTED))

        try:
            self.socket.close()
            for thread in self.threads:
                thread.join(10)
                if thread.is_alive():
                    self.on_event(Event(EventType.THREAD_WARNING, {"thread": thread}))
        except Exception as e:
            self.on_event(Event(EventType.ERROR, {"exception": e}))
        finally:
            self.threads.clear()  # Ensure thread list is cleaned up

class Client:
    """A client - it can receive and send data across a network of a server and clients."""
    def __init__(self, key: bytes | None, hmac_key: bytes | None, address: tuple[str | None, int], on_event: Callable[[Event], Any]):
        """Create a new client."""
        self.socket = simple_socket(SecureMessage(key, hmac_key))
        self.address: _Address = address
        self.threads: list[Thread] = []
        self.on_event: Callable[[Event], Any] = on_event

        self.active: bool = False
    
    def send(self, data: ReadableBuffer, flags: int = 0, /) -> None:
        """Send something to the server."""
        self.socket.sendall(data, flags)
    
    @overload
    def sendto(self, data: ReadableBuffer, address: _RetAddress, /) -> None: ...
    
    @overload
    def sendto(self, data: ReadableBuffer, flags: int, address: _RetAddress, /) -> None: ...
    
    def sendto(self, data: ReadableBuffer, *args: Any) -> None:
        """Send to a specific address."""
        if len(args) == 1:  # Address only
            address = args[0]
            self.socket.sendto(self.socket.encryptor.pack(data), address)
        elif len(args) == 2:  # Flags and address
            flags, address = args
            self.socket.sendto(self.socket.encryptor.pack(data), flags, address)
        else:
            raise ValueError("Invalid arguments")
    
    def init(self) -> None:
        """Connect to the server."""
        # Start client
        self.socket.connect(self.address)

        self.active = True
        
        # Start listener
        listen_thread = Thread(target = self._listen)
        self.threads.append(listen_thread)
        listen_thread.start()

        self.on_event(Event(EventType.CONNECTED))
    
    def _listen(self, reconnect_attempts: int = 3) -> None:
        attempt = 0
        while attempt < reconnect_attempts:
            try:
                while self.active:
                    data = self.socket.recv()
                    self.on_event(Event(EventType.RECEIVED, {"data": data}))
                return  # Return if no errors
            except (ConnectionError, TimeoutError, PacketSizeError) as e:
                self.on_event(Event(EventType.ERROR, {"exception": e}, close=self.close))
                break  # Give up if a critical error occurs
            except Exception as e:
                attempt += 1
                if attempt >= reconnect_attempts:
                    self.on_event(Event(EventType.ERROR, {"exception": e}, close=self.close))
                    break  # Give up after max attempts

                self.on_event(Event(EventType.THREAD_WARNING, {"message": "Reconnecting..."}))

                # Close old connection before re-initializing
                self.close()
                time.sleep(2)  # Prevent reconnect spam
                self.init()  # Try reconnecting
    
    def keep_alive(self, interval: float = 10) -> None:
        """Send a keep-alive message every `interval` seconds."""
        while self.active:
            try:
                self.send(b"KEEP_ALIVE")
                time.sleep(interval)
            except Exception:
                break  # Stop if there's an issue
    
    def close(self) -> None:
        """Close the client."""
        self.active = False  # Stop all operations
        if not hasattr(self, "_disconnected"):  # Prevent duplicate event
            self._disconnected = True  
            self.on_event(Event(EventType.DISCONNECTED))

        try:
            self.socket.close()
            for thread in self.threads:
                thread.join(10)
                if thread.is_alive():
                    self.on_event(Event(EventType.THREAD_WARNING, {"thread": thread}))
        except Exception as e:
            self.on_event(Event(EventType.ERROR, {"exception": e}))
        finally:
            self.threads.clear()  # Ensure thread list is cleaned up

generate_key: Callable[[], bytes] = Fernet.generate_key
generate_hmac_key: Callable[[], bytes] = lambda: secrets.token_bytes(32)
 
# Cleanup
del ReadOnlyBuffer, WriteableBuffer, ReadableBuffer, _Address, _RetAddress