import can
import time

from configs.can_ids import *

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] CAN IDS Started")

door_events = []

while True:

    msg = bus.recv()

    current_time = time.time()

    if msg.arbitration_id == DOOR_ID:

        door_events.append(current_time)

        door_events = [
            t for t in door_events
            if current_time - t < 2
        ]

        if len(door_events) > 5:

            print(
                "[ALERT] Possible Door ECU Spoofing!"
            )

        status = (
            "LOCKED"
            if msg.data[0] == 1
            else "UNLOCKED"
        )

        print(
            f"[Door Event] {status}"
        )