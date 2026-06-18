import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="AutoRed Dashboard",
    layout="wide"
)

st_autorefresh(
    interval=1000,
    key="dashboard_refresh"
)

st.title("🚗 AutoRed Vehicle Dashboard")

try:

    with open(
        "data/vehicle_state.json",
        "r"
    ) as f:

        state = json.load(f)

except:

    state = {
        "speed": 0,
        "rpm": 0,
        "door": "UNKNOWN",
        "brake": "UNKNOWN"
    }

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Speed",
        f"{state['speed']} mph"
    )

    st.metric(
        "RPM",
        state["rpm"]
    )

with col2:

    st.metric(
        "Door Status",
        state["door"]
    )

    st.metric(
        "Brake Status",
        state["brake"]
    )

st.divider()

st.subheader("Security Status")

st.success(
    f"Threat Level: {state.get('threat_level', 'NORMAL')}"
)

alerts = state.get(
    "alerts",
    []
)

if alerts:

    for alert in alerts:

        st.error(alert)

else:

    st.info(
        "No active alerts"
    )