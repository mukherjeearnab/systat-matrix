from cryptography.fernet import Fernet
from pathlib import Path

def get_credentials():
    key = (Path.home() / ".systat_key").read_bytes()
    f = Fernet(key)

    encrypted = Path("systatcreds.enc").read_bytes()
    plaintext = f.decrypt(encrypted).decode()

    username, password = plaintext.split(":", 1)
    print("username =", username)
    # use password securely, don't print it!
    return username, password


def get_room():
    key = (Path.home() / ".systat_key").read_bytes()
    f = Fernet(key)

    encrypted = Path("systat_room.enc").read_bytes()
    plaintext = f.decrypt(encrypted).decode()

    return plaintext



if __name__ == '__main__':
    print(get_credentials())
    print(get_room())
