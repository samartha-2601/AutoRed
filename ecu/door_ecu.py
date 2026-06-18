import can
import random
import time

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

locked = True

print("[+] Door ECU Started")

while True:

    if random.randint(1, 10) > 7:
        locked = not locked

    value = 1 if locked else 0

    msg = can.Message(
        arbitration_id=0x200,
        data=bytes([value]),
        is_extended_id=False
    )

    bus.send(msg)

    state = "LOCKED" if locked else "UNLOCKED"

    print(f"[Door ECU] {state}")

    time.sleep(2)