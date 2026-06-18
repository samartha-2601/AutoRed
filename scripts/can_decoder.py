import can

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] CAN Decoder Started")

while True:

    msg = bus.recv()

    if msg.arbitration_id == 0x100:

        speed = int.from_bytes(
            msg.data,
            byteorder="big"
        )

        print(f"[Speed] {speed} mph")

    elif msg.arbitration_id == 0x101:

        rpm = int.from_bytes(
            msg.data,
            byteorder="big"
        )

        print(f"[RPM] {rpm}")

    elif msg.arbitration_id == 0x200:

        status = (
            "LOCKED"
            if msg.data[0] == 1
            else "UNLOCKED"
        )

        print(f"[Door] {status}")

    elif msg.arbitration_id == 0x300:

        status = (
            "PRESSED"
            if msg.data[0] == 1
            else "RELEASED"
        )

        print(f"[Brake] {status}")