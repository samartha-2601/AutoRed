import can

from configs.can_ids import *

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] CAN Decoder Started")

while True:

    msg = bus.recv()

    if msg.arbitration_id == SPEED_ID:

        speed = int.from_bytes(
            msg.data,
            byteorder="big"
        )

        print(f"[Speed] {speed} mph")

    elif msg.arbitration_id == RPM_ID:

        rpm = int.from_bytes(
            msg.data,
            byteorder="big"
        )

        print(f"[RPM] {rpm}")

    elif msg.arbitration_id == DOOR_ID:

        status = (
            "LOCKED"
            if msg.data[0] == 1
            else "UNLOCKED"
        )

        print(f"[Door] {status}")

    elif msg.arbitration_id == BRAKE_ID:

        status = (
            "PRESSED"
            if msg.data[0] == 1
            else "RELEASED"
        )

        print(f"[Brake] {status}")