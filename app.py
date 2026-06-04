import streamlit as st
import pandas as pd
import json
import os

st.title("🛍️ Purplle Store Intelligence Dashboard")

# ---------- SAFE FILE PATH (WORKS LOCAL + STREAMLIT CLOUD) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENT_FILE = os.path.join(BASE_DIR, "..", "output", "events.jsonl")

events = []

# ---------- LOAD DATA ----------
if not os.path.exists(EVENT_FILE):
    st.warning("No events found. Please ensure output/events.jsonl exists in the repository.")
    st.stop()

with open(EVENT_FILE, "r") as f:
    for line in f:
        if line.strip():  # avoids empty lines
            events.append(json.loads(line))

# ---------- DATAFRAME ----------
df = pd.DataFrame(events)

if df.empty:
    st.warning("Event file is empty.")
    st.stop()

# ---------- BASIC PROCESSING ----------
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# ---------- METRICS ----------
total_events = len(df)
unique_visitors = df["visitor_id"].nunique()

event_counts = df["event_type"].value_counts()

billing_count = len(df[df["event_type"] == "BILLING"])

conversion_rate = (
    (billing_count / unique_visitors) * 100
    if unique_visitors > 0
    else 0
)

# ---------- UI ----------
col1, col2, col3 = st.columns(3)

col1.metric("Total Events", total_events)
col2.metric("Unique Visitors", unique_visitors)
col3.metric("Conversion Rate", f"{conversion_rate:.1f}%")

st.subheader("📊 Event Distribution")
st.bar_chart(event_counts)

st.subheader("📋 Event Counts Table")
st.dataframe(event_counts.reset_index().rename(columns={"index": "Event Type", "event_type": "Count"}))

st.subheader("🕒 Recent Events")
st.dataframe(df.tail(20))