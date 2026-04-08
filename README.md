# Options Trading Dashboard

An interactive options analytics app built with Dash, Plotly, and Python.

It includes:
- live price tracking with intraday candlesticks
- option Greek visualizations
- options chain and volatility views
- open interest and volume analytics
- a PnL strategy builder
- a Learn page with chart explanations

## Tech Stack

- Python
- Dash
- Plotly
- pandas / NumPy / SciPy
- yfinance
- Docker

## Requirements

For local Python runs:
- Python 3.10+ recommended
- `pip`

For Docker runs:
- Docker
- Docker Compose

## Run With Docker

From the project root:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8050
```

The container also exposes port `8888`, but the dashboard itself runs on `8050`.

## Run Locally With Python

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python3 app.py
```

4. Open the dashboard:

```text
http://localhost:8050
```

## Notes

- Market and options data comes from `yfinance`.
- Because of Yahoo data limits, some options-related charts may load slowly or occasionally return sparse data.
- The app refreshes live data on a short interval, so temporary rate limiting can affect chart responsiveness.
- If Docker is already running an older container, rebuild with `docker compose up --build` after pulling new changes.

## Project Structure

```text
.
├── app.py
├── assets/
├── components/
├── data/
├── models/
├── pages/
├── requirements.txt
└── docker-compose.yml
```

## Troubleshooting

If the app does not start locally:
- make sure your virtual environment is activated
- confirm dependencies installed successfully with `pip install -r requirements.txt`
- check that port `8050` is not already in use

If charts are missing data:
- try a different ticker
- wait a few seconds and refresh
- keep in mind that some options chains from Yahoo can be sparse or rate-limited
