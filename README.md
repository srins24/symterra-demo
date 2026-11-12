# Site Operations Dashboard (Demo)

A demo project that connects a live external data feed to a site operations data model and monitors the feed through a dashboard. Built in Python, SQL and Streamlit.

**Live demo:** https://symterra-demo-m5tcubpoyfr23szkfbdcst.streamlit.app

> All client, site, asset, work order and operative data is fictional. The weather readings come from the public Open-Meteo API. This is demo work for integration and monitoring, not client work.

## Quick tour (2 minutes)

1. Open the live demo. The first section shows current weather for two sites, with the observation time.
2. Scroll to **Open work by priority** and **Work orders by month** to see the operations view built from SQL views.
3. Look at **Integration health** and **Last sync runs** to see how each data source is monitored: run counts, failures, rows received and rejected, and error messages.

The weather on the hosted demo is a snapshot from the last database update. The live feed runs on a local machine on an hourly schedule.

## What this project demonstrates

- **Data modelling:** a relational SQLite schema covering clients, sites, assets, work orders with status history, operatives, form templates and submissions, integration sources, sync runs, raw records and data quality issues.
- **SQL:** four reporting views (monthly work orders, open work by priority, asset inspection status, integration health) that feed the dashboard.
- **API integration:** a Python feed that pulls data from a public REST API for each site, with retries and exponential backoff.
- **Data quality and monitoring:** every run is logged with its status and row counts. Raw responses are stored so readings can be re-derived. Failed calls and rejected readings are recorded, not silently dropped.
- **Idempotent loads:** re-running a sync updates existing readings instead of duplicating them.
- **Testing:** offline tests run the feed against a recorded API response, covering repeat runs, a rejected reading and a no-network failure.
- **Dashboarding:** a read-only Streamlit app that shows a clear error if the database file is missing.

## Tech stack

- Python: `sqlite3`, `urllib`, `argparse`, pandas
- SQLite with portable SQL (schema, seed data, views)
- Streamlit for the dashboard
- Windows Task Scheduler for the hourly local feed

## Running it locally

```bash
pip install streamlit pandas
python ingest.py --db symterra.db                                              # live weather sync (needs internet)
python ingest.py --db symterra.db --from-file fixtures/open_meteo_sample.json  # offline sample
streamlit run dashboard.py -- --db symterra.db
```

## Notes

- Open-Meteo's free tier is for non-commercial use.
- The monitoring views show some failed and partial sync runs from the sample data, so the failure handling is visible.

## Repository contents

- `dashboard.py`: Streamlit dashboard
- `requirements.txt`: Python dependencies
- `symterra.db`: built database with fictional seed data and the latest weather readings
- `README.md`: this file
