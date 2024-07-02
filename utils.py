import socket
import getpass


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
        return IP
    except Exception as e:
        print(f"Error getting IP: {e}")
        return None


def get_username():
    return getpass.getuser()
