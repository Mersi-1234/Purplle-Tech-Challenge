import streamlit as st
import pandas as pd
import json
from collections import Counter

st.title("🛍️ Purplle Store Intelligence Dashboard")

EVENT_FILE = "output/events.jsonl"

events = []

try:

    with open(EVENT_FILE, "r") as f:

        for line in f:
            events.append(json.loads(line))

except FileNotFoundError:

    st.warning("No events found.")
    st.stop()

df = pd.DataFrame(events)

total_events = len(df)

unique_visitors = df["visitor_id"].nunique()

event_counts = df["event_type"].value_counts()

billing_count = len(df[df["event_type"] == "BILLING"])

conversion_rate = (
    billing_count / unique_visitors * 100
    if unique_visitors > 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", total_events)
col2.metric("Unique Visitors", unique_visitors)
col3.metric("Conversion Rate", f"{conversion_rate:.1f}%")

st.subheader("Event Distribution")

st.bar_chart(event_counts)

st.subheader("Event Counts")

st.dataframe(event_counts.reset_index())

st.subheader("Recent Events")

st.dataframe(df.tail(20))