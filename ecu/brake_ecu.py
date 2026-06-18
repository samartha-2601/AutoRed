import can
import random
import time

from configs.can_ids import *

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

brake_pressed = False

print("[+] Brake ECU Started")

while True:

    if random.randint(1, 10) > 7:
        brake_pressed = not brake_pressed

    value = 1 if brake_pressed else 0

    msg = can.Message(
        arbitration_id=BRAKE_ID,
        data=bytes([value]),
        is_extended_id=False
    )

    bus.send(msg)

    state = "PRESSED" if brake_pressed else "RELEASED"

    print(f"[Brake ECU] {state}")

    time.sleep(1)