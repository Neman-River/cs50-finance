# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CS50 Finance — a Flask web app for managing a simulated stock portfolio. Users can register, look up stock quotes, buy/sell shares, and view transaction history.

## Running the App

```bash
# Install dependencies
uv add cs50 Flask Flask-Session pytz requests

# Run development server
flask run
```

App runs at `http://localhost:5000`.

## Architecture

- **app.py** — All Flask routes and business logic
- **helpers.py** — Utility functions: `apology()`, `login_required` decorator, `lookup()` (external stock API), `usd()` Jinja2 filter
- **finance.db** — SQLite database with `users` and `transactions` tables
- **templates/** — Jinja2 templates, all extending `layout.html`

### Database Schema

```sql
-- users table is managed by CS50 scaffolding
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    stock TEXT NOT NULL,
    price REAL NOT NULL,
    shares INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Key Patterns

- **Auth**: Session-based; `session["user_id"]` stores the logged-in user. Routes protected with `@login_required`.
- **Database**: CS50's `SQL` wrapper — `db.execute("SELECT ...", arg)` returns list of dicts.
- **Stock data**: `lookup(symbol)` fetches from `https://finance.cs50.io/quote`, returns `{"name", "price", "symbol"}` or `None`.
- **Errors**: `apology(message, code)` renders `apology.html` with a meme from memegen.link.
- **Currency**: Use `usd()` filter in templates (`{{ value | usd }}`).
- **Sessions**: Stored on filesystem in `flask_session/` (not cookies).

## Dependencies

Uses CS50's `SQL` wrapper (not SQLAlchemy). All packages listed in `requirements.txt`. Use `uv` to manage packages per global preferences.
