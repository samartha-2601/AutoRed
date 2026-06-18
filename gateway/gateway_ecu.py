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
    "alerts": [],
    "blocked_messages": 0,
    "attack_type": "NONE"
}

door_events = []

alert_active = False
block_door_messages = False

print("[+] Gateway ECU Started")

while True:

    msg = bus.recv()

    current_time = time.time()

    # -------------------------
    # Speed
    # -------------------------

    if msg.arbitration_id == SPEED_ID:

        vehicle_state["speed"] = int.from_bytes(
            msg.data,
            byteorder="big"
        )

    # -------------------------
    # RPM
    # -------------------------

    elif msg.arbitration_id == RPM_ID:

        vehicle_state["rpm"] = int.from_bytes(
            msg.data,
            byteorder="big"
        )

    # -------------------------
    # Door ECU
    # -------------------------

    elif msg.arbitration_id == DOOR_ID:

        if block_door_messages:

            security_state["blocked_messages"] += 1

            continue

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

        if len(door_events) > 5 and not alert_active:

            security_state["threat_level"] = "HIGH"

            security_state["alerts"] = [
                "Door ECU Replay/Spoofing Detected"
            ]

            security_state["attack_type"] = (
                "REPLAY / SPOOFING"
            )

            with open(
                "logs/security_events.log",
                "a"
            ) as f:

                f.write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')} "
                    "Door ECU Replay/Spoofing Detected\n"
                )

            alert_active = True

            block_door_messages = True

            with open(
                "logs/security_events.log",
                "a"
            ) as f:

                f.write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')} "
                    "Gateway Blocking Activated\n"
                )

    # -------------------------
    # Brake ECU
    # -------------------------

    elif msg.arbitration_id == BRAKE_ID:

        vehicle_state["brake"] = (
            "PRESSED"
            if msg.data[0] == 1
            else "RELEASED"
        )

    # -------------------------
    # Write Vehicle State
    # -------------------------

    with open(
        "data/vehicle_state.json",
        "w"
    ) as f:

        json.dump(
            vehicle_state,
            f,
            indent=4
        )

    # -------------------------
    # Write Security State
    # -------------------------

    with open(
        "data/security_state.json",
        "w"
    ) as f:

        json.dump(
            security_state,
            f,
            indent=4
        )