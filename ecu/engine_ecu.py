import can
import random
import time

# Connect to virtual CAN interface
bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

speed = 60
rpm = 2500

print("[+] Engine ECU Started")
print("[+] Sending CAN messages on vcan0")

while True:

    # Simulate vehicle movement
    speed += random.randint(-2, 2)
    rpm += random.randint(-100, 100)

    speed = max(0, speed)
    rpm = max(700, rpm)

    # CAN ID 0x100 = Speed
    speed_msg = can.Message(
        arbitration_id=0x100,
        data=speed.to_bytes(2, byteorder="big"),
        is_extended_id=False
    )

    # CAN ID 0x101 = RPM
    rpm_msg = can.Message(
        arbitration_id=0x101,
        data=rpm.to_bytes(2, byteorder="big"),
        is_extended_id=False
    )

    bus.send(speed_msg)
    bus.send(rpm_msg)

    print(
        f"[Engine ECU] "
        f"Speed={speed} mph "
        f"RPM={rpm}"
    )

    time.sleep(1)