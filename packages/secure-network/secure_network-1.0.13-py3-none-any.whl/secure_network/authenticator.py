"""
A simple authenticator over the network. Enjoy, as this was hard!
"""

from .network import Event, EventType, Client, Server
from typing import Callable, Union, Optional, Any, TypeAlias
from collections.abc import Buffer, Iterable
from cryptography.fernet import Fernet
import json
import os
import hashlib
import secrets
import time
import socket
import hmac
import bcrypt 
import pyotp
import smtplib
import requests
import logging

logger = logging.getLogger(__name__)

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

class SERVER(Server): 
    """Secure authentication server with session management & role-based access control."""

    def __init__(self, key: bytes | None, hmac_key: bytes | None, address: _Address, on_event: Callable[[Event], Any], max_clients: Optional[int] = None):
        super().__init__(key, hmac_key, address, self._intercept_event, max_clients)
        self.on_event_callback: Callable[[Event], Any] = on_event

        # Load accounts from file
        self.accounts_file: str = "accounts.json"
        self.accounts: dict = self._load_accounts()

        # Generate encryption key for session tokens
        self.token_cipher: Fernet = Fernet(Fernet.generate_key())

        self.failed_logins: dict[_RetAddress, list[float]] = {}  # {IP: [timestamps]}
        self.RATE_LIMIT: int = 5  # Max failed attempts
        self.BLOCK_TIME: float = 60  # Block duration in seconds

        self.GMAIL: dict[str, str] = {"gmail": "user@example.com", "password": "your_password"}
        self.TEXTLOCAL_API_KEY: str = "TEXTLOCAL_API_KEY"

        self.mfa_enabled_users: dict[str, dict[str, str]] = {}  # {username: {"secret": TOTP_SECRET, "method": "email" or "sms", "contact": "email_or_phone"}}

    def _encrypt_token(self, token: str) -> str:
        """Encrypt a session token for secure storage."""
        return self.token_cipher.encrypt(token.encode()).decode()

    def _decrypt_token(self, token: str) -> str:
        """Decrypt a session token."""
        return self.token_cipher.decrypt(token.encode()).decode()

    def _generate_token(self) -> str:
        """Generate a secure session token and hash it with HMAC."""
        raw_token = secrets.token_hex(16)  # Generate a random token
        token_hmac = hmac.new(self.socket.encryptor._generate_hmac(raw_token.encode()), raw_token.encode(), hashlib.sha256).hexdigest()
        return f"{raw_token}:{token_hmac}"  # Store both the raw token and the hashed token

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt for secure storage."""
        salt = bcrypt.gensalt()  # Generate a new salt
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def _has_permission(self, username: str, required_role: str) -> bool:
        """Check if a user has the required role to perform an action."""
        return self.accounts.get(username, {}).get("role") == required_role

    def create_account(self, username: str, password: str, role: str = "user", mfa_method: str = None, contact: str = None) -> bool:
        """Register a new user with a role (default: user)."""
        if username in self.accounts:
            return False  # Username already exists

        self.accounts[username] = {
            "password": self._hash_password(password),
            "role": role.lower()
        }

        if mfa_method in ["email", "sms"]:
            totp_secret = pyotp.random_base32()
            self.mfa_enabled_users[username] = {"secret": totp_secret, "method": mfa_method, "contact": contact}
            logger.info(f"🔐 MFA enabled for {username} via {mfa_method}")

        self._save_accounts()
        return True
    
    def logout(self, username: str) -> bool:
        """Log out a user by invalidating their session token."""
        if username in self.accounts and "token" in self.accounts[username]:
            del self.accounts[username]["token"]
            del self.accounts[username]["token_expiry"]
            self._save_accounts()
            logger.info(f"🔴 {username} has logged out.")
            return True
        return False
    
    def _cleanup_expired_sessions(self):
        """Remove expired session tokens."""
        current_time = time.time()
        for username, user_data in list(self.accounts.items()):
            if "token_expiry" in user_data and user_data["token_expiry"] < current_time:
                logger.info(f"Session expired for {username}, logging out.")
                self.logout(username)
    
    def _is_valid_session(self, username: str, token: str) -> bool:
        """Verify if the provided token is valid and untampered with."""
        if not token: 
            logger.debug("Token was not proper.")
            return False

        user = self.accounts.get(username)
        if not user or "token" not in user:
            logger.debug(f"No token found for {username}")
            return False

        stored_token = user["token"]  # Full format: raw_token:hmac_hash
        stored_raw_token, stored_token_hmac = stored_token.split(":") # In case of further need
        received_raw_token, received_hmac = token.split(":")  # Extract both parts

        # Verify HMAC
        calculated_hmac = hmac.new(self.socket.encryptor._generate_hmac(received_raw_token.encode()), received_raw_token.encode(), hashlib.sha256).hexdigest()

        if received_hmac != calculated_hmac:
            logger.warning(f"Token verification failed for {username}")
            return False  # Token has been tampered with

        return True
    
    def _load_accounts(self) -> dict:
        """Load accounts from a JSON file (persistent storage)."""
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                return json.load(f)
        return {}

    def _save_accounts(self) -> None:
        """Save accounts to a JSON file (persistent storage)."""
        with open(self.accounts_file, "w") as f:
            json.dump(self.accounts, f, indent=4)
    
    def _send_sms(self, phone_number: str, code: str):
        """Send an MFA code via SMS."""
        api_key = self.TEXTLOCAL_API_KEY
        message = f"Your MFA code is: {code}"
        sender = "AuthSystem"

        url = f"https://api.textlocal.com/send/?apikey={api_key}&numbers={phone_number}&message={message}&sender={sender}"
        
        try:
            response = requests.get(url)
            logger.info(f"📲 MFA code sent to {phone_number}: {response.json()}")
        except Exception as e:
            logger.warning(f"⚠️ Error sending SMS: {e}")
    
    def _send_email(self, recipient: str, code: str):
        """Send an MFA code via email."""
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = self.GMAIL["gmail"]
        sender_password = self.GMAIL["password"]

        subject = "Your MFA Code"
        message = f"Your MFA code is: {code}"

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, f"Subject: {subject}\n\n{message}")
            server.quit()
            logger.info(f"📧 MFA code sent to {recipient}")
        except Exception as e:
            logger.warning(f"⚠️ Error sending email: {e}")
    
    def _send_mfa_code(self, username: str):
        """Generate and send a TOTP-based MFA code via email or SMS."""
        if username not in self.mfa_enabled_users:
            return

        user_mfa = self.mfa_enabled_users[username]
        totp = pyotp.TOTP(user_mfa["secret"])
        code = totp.now()

        if user_mfa["method"] == "email":
            self._send_email(user_mfa["contact"], code)
        elif user_mfa["method"] == "sms":
            self._send_sms(user_mfa["contact"], code)

    def _intercept_event(self, event: Event) -> None:
        """Intercept and process authentication-related events before handling other actions."""
        if event.type == EventType.RECEIVED:
            try:
                data = json.loads(event.data["data"].decode())
                username = data.get("username")
                token = data.get("token")
                password = data.get("password")
                addr: _RetAddress = event.data.get("address")
                conn: socket.socket = event.data.get("connection")

                if not addr:
                    logger.warning("⚠️ No address found for sendto(). Dropping message.")
                    return  # Prevent crash

                # Print debug info
                logger.debug(f"Debug: Received data for user {username}")
                if token:
                    logger.debug(f"Debug: Token provided: {token}")
                    if username in self.accounts:
                        logger.debug(f"Debug: Stored token: {self.accounts[username].get('token')}")

                # Handle logout
                if data.get("logout"):
                    self.logout(username)
                    self.on_event_callback(Event(EventType.DISCONNECTED, {"username": username}))
                    return
                
                if data.get("mfa_code"):
                    if username in self.mfa_enabled_users:
                        totp = pyotp.TOTP(self.mfa_enabled_users[username]["secret"])
                        if totp.verify(data["mfa_code"]):
                            logger.info(f"✅ MFA success for {username}")
                        else:
                            logger.info(f"❌ Incorrect MFA code for {username}")
                            conn.sendall(json.dumps({"status": "error", "message": "Invalid MFA code"}).encode())
                            return

                # Initial authentication (no token yet)
                if username and password and not token:
                    ip_address = addr[0]  # Extract IP from address tuple
                    
                    # Cleanup old failed attempts
                    self.failed_logins.setdefault(ip_address, [])
                    self.failed_logins[ip_address] = [
                        t for t in self.failed_logins[ip_address] if t > time.time() - self.BLOCK_TIME
                    ]

                    if len(self.failed_logins[ip_address]) >= self.RATE_LIMIT:
                        logger.info(f"🚫 Too many failed attempts from {ip_address}. Blocking for {self.BLOCK_TIME} seconds.")
                        conn.sendall(self.socket.encryptor.pack(json.dumps({"status": "error", "message": "Too many failed attempts. Try again later."}).encode()))
                        return
    
                    if username in self.accounts and bcrypt.checkpw(password.encode(), self.accounts[username]["password"].encode()):
                        logger.info(f"✅ Authentication success for {username}")

                        if username in self.mfa_enabled_users:
                            logger.info(f"🔐 MFA required for {username}")
                            self._send_mfa_code(username)
                            conn.sendall(json.dumps({"status": "mfa_required", "message": "Enter your MFA code"}).encode())
                            return  # Stop here and wait for MFA code

                        # Reset failed attempts after successful login
                        self.failed_logins[ip_address] = []

                        # Generate session token
                        session_token = self._generate_token()
                        self.accounts[username]["token"] = session_token
                        self.accounts[username]["token_expiry"] = time.time() + 3600  # Valid for 1 hour
                        self._save_accounts()

                        logger.debug(f"Debug: Generated new token: {session_token}")  # Debug line

                        # Send session token to client
                        response = json.dumps({"status": "success", "username": username, "token": session_token}).encode()
                        conn.sendall(self.socket.encryptor.pack(response))
                        return
                    else:
                        logger.info(f"❌ Authentication failed for {username}")
                        self.failed_logins[ip_address].append(time.time())  # Log failed attempt
                        self.on_event_callback(Event(EventType.ERROR, {"exception": "Invalid credentials"}))
                        return

                # Handle regular messages (with token)
                if "message" in data:
                    if self._is_valid_session(username, token):
                        # Create new event with the message and user context
                        new_event = Event(EventType.RECEIVED, 
                            {"data": data["message"].encode(), "username": username, "token": token}
                        )
                        self.on_event_callback(new_event)
                        return
                    else:
                        logger.warning(f"❌ Unauthorized message from {username}")
                        self.on_event_callback(Event(EventType.ERROR, {"exception": "Invalid or expired session"}))
                        return

            except Exception as e:
                logger.error(f"⚠️ Error processing message: {e.__class__.__name__}: {str(e)} (steams from line {e.__traceback__.tb_lineno})")
                return
        
        # Pass non-RECIEVED events to the actual event handler
        self.on_event_callback(event)

class CLIENT(Client): 
    """Client implementation with authentication handling and session management."""

    def __init__(self, key: bytes | None, hmac_key: bytes | None, address: _Address, on_event: Callable[[Event], Any]):
        super().__init__(key, hmac_key, address, self._intercept_event)
        self.on_event_callback: Callable[[Event], Any] = on_event
        self.username: str = ""
        self.password: str = ""
        self.token: Optional[str] = None  # Store session token
    
    def is_token_valid(self) -> bool:
        """Check if the stored token is valid (not expired)."""
        if not self.token:
            return False
        # Additional expiration checks can be added here
        return True

    def _intercept_event(self, event: Event) -> None:
        """Intercept server events and handle authentication responses."""
        if event.type == EventType.RECEIVED:
            try:
                data = json.loads(event.data["data"].decode())
                if data.get("status") == "success":
                    self.token = data["token"]
                    logger.info(f"✅ Authenticated! Token received: {self.token}")
                else:
                    logger.info(f"❌ Authentication failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError as e:
                logger.debug("Data was not server response, parsing through.")
            except Exception as e:
                logger.error(f"⚠️ Error processing server response: {e.__class__.__name__}: {str(e)} (steams from line {e.__traceback__.tb_lineno})")
                return
        self.on_event_callback(event)
    
    def auth(self, username: str, password: str) -> None:
        """Send authentication request to the server."""
        self.username = username
        self.password = password
        
        # Create authentication packet
        auth_data = json.dumps({
            "username": username,
            "password": password
        }).encode()
        
        self.send(auth_data)
    
    def send(self, data: ReadableBuffer, flags: int = 0, /) -> None:
        """Send a message with session info if authenticated."""
        try:
            # If it's already JSON data (like auth), send as is
            json.loads(data.decode())
            super().send(data, flags)
        except json.JSONDecodeError:
            # For regular messages, include session info
            message_data = json.dumps({
                "username": self.username,
                "token": self.token,
                "message": data.decode()
            }).encode()
            super().send(message_data, flags)
    
    def logout(self) -> None:
        """Log out by sending a logout request to the server."""
        if self.token:
            logout_data = json.dumps({
                "username": self.username,
                "token": self.token,
                "logout": True
            }).encode()
            self.send(logout_data)
            logger.info(f"🔴 Logged out: {self.username}")

AuthSocket: Union[Server, Client] = Union[SERVER, CLIENT]

# Cleanup
del ReadOnlyBuffer, WriteableBuffer, ReadableBuffer, _Address, _RetAddress