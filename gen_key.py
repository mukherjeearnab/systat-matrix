from cryptography.fernet import Fernet
from pathlib import Path

keyfile = Path.home() / ".systat_key"
if not keyfile.exists():
    key = Fernet.generate_key()
    keyfile.write_bytes(key)
    keyfile.chmod(0o600)   # only owner can read/write
