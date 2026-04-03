# Finance

A web application for managing a simulated stock portfolio. Built as the final project for Week 9 of [CS50x](https://cs50.harvard.edu/x/) — Introduction to Computer Science by Harvard University.

## About the App

Finance is a paper trading simulator — it lets you practice buying and selling stocks without using real money. Each new user starts with $10,000 in virtual cash. You can search for any real stock by its ticker symbol, see the current price, and decide how many shares to buy. Your portfolio updates in real time, showing the current value of every position alongside your remaining cash. When you're ready to sell, you choose a stock you own and how many shares to offload, and the cash is credited back to your balance. Every transaction is recorded, so you can always review your full trading history.

The app uses real stock price data fetched live from an external API, so the prices you see reflect actual market values.

## Features

- **Register / Login** — Create a personal account; passwords are stored securely using hashing
- **Quote** — Look up the current price of any stock by entering its ticker symbol (e.g. AAPL, TSLA)
- **Buy** — Purchase shares of a stock; the cost is deducted from your cash balance
- **Sell** — Sell shares you own; proceeds are added back to your cash balance
- **Portfolio** — Overview of all your current holdings with live prices, number of shares, position value, and total account value
- **History** — Full chronological log of every buy and sell transaction with timestamps
- **Settings** — Change your account password

## Tech Stack

- **Python / Flask** — Backend web framework
- **SQLite** — Database for users and transactions
- **Jinja2** — HTML templating
- **Bootstrap 5** — Frontend styling
- **Werkzeug** — Password hashing
- **CS50 SQL library** — Database access layer

Stock data is fetched from the [CS50 Finance API](https://finance.cs50.io/).

## Running Locally

```bash
# Create virtual environment and install dependencies
uv venv && uv pip install -r requirements.txt

# Start the development server
flask run
```

App will be available at `http://127.0.0.1:5000`.

## About

This project was completed as part of **CS50x** (CS50's Introduction to Computer Science), a free online course offered by Harvard University. The course covers the foundations of computer science including programming in C, Python, SQL, and web development.
