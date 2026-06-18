import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AutoRed Dashboard",
    layout="wide"
)

# Auto refresh every second
st_autorefresh(
    interval=1000,
    key="dashboard_refresh"
)

# --------------------------------------------------
# Load Vehicle State
# --------------------------------------------------

try:
    with open(
        "data/vehicle_state.json",
        "r"
    ) as f:
        vehicle = json.load(f)

except Exception:
    vehicle = {
        "speed": 0,
        "rpm": 0,
        "door": "UNKNOWN",
        "brake": "UNKNOWN"
    }

# --------------------------------------------------
# Load Security State
# --------------------------------------------------

try:
    with open(
        "data/security_state.json",
        "r"
    ) as f:
        security = json.load(f)

except Exception:
    security = {
        "threat_level": "NORMAL",
        "alerts": []
    }

# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("🚗 AutoRed Vehicle Dashboard")

# --------------------------------------------------
# Vehicle Metrics
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Speed",
        f"{vehicle['speed']} mph"
    )

    st.metric(
        "RPM",
        vehicle["rpm"]
    )

with col2:

    st.metric(
        "Door Status",
        vehicle["door"]
    )

    st.metric(
        "Brake Status",
        vehicle["brake"]
    )

# --------------------------------------------------
# Security Section
# --------------------------------------------------

st.divider()

st.subheader("Security Status")

threat_level = security.get(
    "threat_level",
    "NORMAL"
)

alerts = security.get(
    "alerts",
    []
)

if threat_level == "HIGH":

    st.error(
        f"Threat Level: {threat_level}"
    )

elif threat_level == "MEDIUM":

    st.warning(
        f"Threat Level: {threat_level}"
    )

else:

    st.success(
        f"Threat Level: {threat_level}"
    )

# --------------------------------------------------
# Alerts
# --------------------------------------------------

if alerts:

    for alert in alerts:

        st.error(alert)

else:

    st.info(
        "No active alerts"
    )


# --------------------------------------------------
# Event Feed
# --------------------------------------------------

st.divider()

st.subheader("Recent Security Events")

try:

    with open(
        "logs/security_events.log",
        "r"
    ) as f:

        events = f.readlines()

    events = events[-10:]

    if events:

        for event in reversed(events):

            st.code(event.strip())

    else:

        st.info(
            "No security events recorded"
        )

except:

    st.info(
        "No security events recorded"
    )