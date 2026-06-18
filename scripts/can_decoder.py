import can

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] CAN Decoder Started")

while True:

    message = bus.recv()

    if message.arbitration_id == 0x100:

        speed = int.from_bytes(
            message.data,
            byteorder="big"
        )

        print(
            f"[Speed] {speed} mph"
        )

    elif message.arbitration_id == 0x101:

        rpm = int.from_bytes(
            message.data,
            byteorder="big"
        )

        print(
            f"[RPM] {rpm}"
        )