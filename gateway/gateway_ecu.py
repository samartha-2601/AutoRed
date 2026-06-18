import can
import json
import time

from configs.can_ids import *

bus = can.interface.Bus(
    channel="vcan0",
    interface="socketcan"
)

vehicle_state = {
    "speed": 0,
    "rpm": 0,
    "door": "UNKNOWN",
    "brake": "UNKNOWN"
}

security_state = {
    "threat_level": "NORMAL",
    "alerts": []
}

door_events = []

print("[+] Gateway ECU Started")

while True:

    msg = bus.recv()

    current_time = time.time()

    if msg.arbitration_id == SPEED_ID:

        vehicle_state["speed"] = int.from_bytes(
            msg.data,
            byteorder="big"
        )

    elif msg.arbitration_id == RPM_ID:

        vehicle_state["rpm"] = int.from_bytes(
            msg.data,
            byteorder="big"
        )

    elif msg.arbitration_id == DOOR_ID:

        vehicle_state["door"] = (
            "LOCKED"
            if msg.data[0] == 1
            else "UNLOCKED"
        )

        door_events.append(current_time)

        door_events = [
            t for t in door_events
            if current_time - t < 2
        ]

        if len(door_events) > 5:

            security_state["threat_level"] = "HIGH"

            security_state["alerts"] = [
                "Door ECU Spoofing Detected"
            ]

    elif msg.arbitration_id == BRAKE_ID:

        vehicle_state["brake"] = (
            "PRESSED"
            if msg.data[0] == 1
            else "RELEASED"
        )

    with open(
        "data/vehicle_state.json",
        "w"
    ) as f:

        json.dump(
            vehicle_state,
            f,
            indent=4
        )

    with open(
        "data/security_state.json",
        "w"
    ) as f:

        json.dump(
            security_state,
            f,
            indent=4
        )