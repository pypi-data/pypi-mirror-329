import asyncio
import logging
import sys
import threading
import time

sys.path.append("../")
logging.basicConfig(level=20)

from pysmarlaconnectapi import Connection, ConnectionHub
from pysmarlaconnectapi.federwiege import BabywiegeService

try:
    from config import AUTH_TOKEN_PERSONAL, HOST
except ImportError:
    print("config.py or mandatory variables missing, please add in root folder...")
    exit()

loop = asyncio.get_event_loop()
async_thread = threading.Thread(target=loop.run_forever)

connection = Connection(url=HOST, token_json=AUTH_TOKEN_PERSONAL)

hub = ConnectionHub(loop, connection, interval=10, backoff=0)
babywiege_svc = BabywiegeService(hub)


def main():
    async_thread.start()
    hub.start()

    while not hub.connected:
        time.sleep(1)

    babywiege_svc.sync()

    time.sleep(5)

    value = babywiege_svc.swing_active.get()
    print(f"Swing Active: {value}")

    babywiege_svc.swing_active.set(True)

    time.sleep(1)

    value = babywiege_svc.swing_active.get()
    print(f"Swing Active: {value}")

    time.sleep(5)

    value = babywiege_svc.swing_active.get()
    print(f"Swing Active: {value}")

    input()


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        pass
    hub.stop()
    loop.call_soon_threadsafe(loop.stop)
