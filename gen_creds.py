from cryptography.fernet import Fernet
from pathlib import Path

key = (Path.home() / ".systat_key").read_bytes()
f = Fernet(key)

credentials = b"username:password"
encrypted = f.encrypt(credentials)

Path("systatcreds.enc").write_bytes(encrypted)

room = b"roomid:matrix.org"
encrypted = f.encrypt(room)

Path("systat_room.enc").write_bytes(encrypted)
