"""Live dashboard over the site operations model. Run with: streamlit run dashboard.py -- --db symterra.db"""
import sqlite3, sys
import pandas as pd
import streamlit as st
import altair as alt

import os
from pathlib import Path

st.set_page_config(page_title="Site operations (demo)", layout="wide")  # must be the first Streamlit call

db = (sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv else None) or os.environ.get("SYMTERRA_DB", "symterra.db")
if not Path(db).is_file():
    st.error(f"Database not found: {db}. Pass --db or set SYMTERRA_DB.")
    st.stop()
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)

st.title("Site operations (demo data)")
st.caption("Fictional data. Weather is refreshed by the live feed in ingest.py.")

st.subheader("Current site weather")
st.dataframe(pd.read_sql("SELECT s.site_name, w.observed_at, w.temperature_c, w.wind_speed_kmh "
                         "FROM v_site_weather_latest w JOIN site s ON s.site_id = w.site_id", con), use_container_width=True)

st.subheader("Open work by priority")
open_work = pd.read_sql("SELECT site_id, priority, open_count FROM v_open_work_by_priority", con)
by_priority = open_work.groupby("priority", as_index=False)["open_count"].sum()
order = ["emergency", "high", "medium", "low"]
by_priority["priority"] = pd.Categorical(by_priority["priority"], categories=order, ordered=True)
by_priority = by_priority.sort_values("priority").dropna(subset=["priority"])
chart = (
    alt.Chart(by_priority)
    .mark_bar(size=48, color="#2F6F9F")
    .encode(
        x=alt.X("priority:N", sort=order, title="Priority"),
        y=alt.Y("open_count:Q", title="Open work orders", axis=alt.Axis(tickMinStep=1)),
        tooltip=["priority", "open_count"],
    )
    .properties(height=280)
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Work orders by month")
st.dataframe(pd.read_sql("SELECT * FROM v_work_order_monthly", con), use_container_width=True)

st.subheader("Integration health")
st.dataframe(pd.read_sql("SELECT * FROM v_integration_health", con), use_container_width=True)

st.subheader("Last sync runs")
st.dataframe(pd.read_sql("SELECT sync_run_id, started_at, status, rows_received, rows_rejected, error_message "
                         "FROM integration_sync_run ORDER BY sync_run_id DESC LIMIT 10", con), use_container_width=True)
