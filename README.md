# Finance

A web application for managing a simulated stock portfolio. Built as the final project for Week 9 of [CS50x](https://cs50.harvard.edu/x/) — Introduction to Computer Science by Harvard University.

## Features

- **Register / Login** — Create an account and authenticate securely with hashed passwords
- **Quote** — Look up real-time stock prices by ticker symbol
- **Buy** — Purchase shares using your available cash balance
- **Sell** — Sell shares you currently own
- **Portfolio** — Dashboard showing all holdings with current prices and total value
- **History** — Full log of every buy and sell transaction
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
