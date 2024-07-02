import kthread  # pip install kthread
from time import sleep
import subprocess
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        pass
    finally:
        s.close()
    return IP


print(get_ip())
pool = get_ip().split()[0].rsplit(".", 1)[0]
print(pool)


def getips():
    ipadressen = {}

    def ping(ipadresse):
        try:
            outputcap = subprocess.run(
                [f"ping", ipadresse, "-n", "1"], capture_output=True
            )  # sends only one package, faster
            ipadressen[ipadresse] = outputcap
        except Exception as Fehler:
            print(Fehler)

    t = [
        kthread.KThread(target=ping, name=f"ipgetter{ipend}", args=(f"{pool}.{ipend}",))
        for ipend in range(255)
    ]  # prepares threads
    [kk.start() for kk in t]  # starts 255 threads
    while len(ipadressen) < 255:
        print("Searching network")
        sleep(0.3)
    alldevices = []
    for key, item in ipadressen.items():
        if not "unreachable" in item.stdout.decode(
            "utf-8"
        ) and "failure" not in item.stdout.decode(
            "utf-8"
        ):  # checks if there wasn't neither general failure nor 'unrechable host'
            alldevices.append(key)
    return alldevices


allips = getips()
