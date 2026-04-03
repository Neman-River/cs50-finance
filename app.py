import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd


# CREATE TABLE transactions (
#     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     timestamp TEXT NOT NULL DEFAULT (datetime('now')),
#     stock TEXT NOT NULL,
#     price REAL NOT NULL,
#     shares INTEGER NOT NULL,
#     user_id INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # """Show portfolio of stocks"""
    stock_dicts = db.execute(
        "SELECT stock, SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY stock", session["user_id"])

    stocks_total = 0
    for asset in stock_dicts:

        price = lookup(asset["stock"])["price"]
        total = asset["shares"] * price

        asset["price"] = price
        asset["total"] = total

        stocks_total += total

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    grand_total = stocks_total + cash

    return render_template("index.html", stocks=stock_dicts, cash=cash, total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # validate symbol input:
        if not symbol:
            return apology("must provide a symbol")

        # validate shares input:
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer")

        shares = int(shares)

        # check if the symbol exists:
        try:
            price = lookup(symbol)["price"]
        except:
            return apology("incorrect symbol")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        cost = price * shares

        if cash >= cost:
            db.execute("INSERT INTO transactions (stock, price, shares, user_id) VALUES (?, ?, ?, ?)",
                       symbol, price, shares, session["user_id"])
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ? ", cost, session["user_id"])
            return redirect("/")
        else:
            return apology("not enough money")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_info = db.execute(
        "SELECT timestamp, stock, price, shares FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", history_info=history_info)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change Password"""

    if request.method == "POST":

        row = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        old_password = request.form.get("old_password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not old_password:
            return apology("must provide an old password", 403)
        if not password:
            return apology("must provide new password", 403)
        if not confirmation:
            return apology("must repeat new password", 403)

        # Ensure old password is correct
        if not check_password_hash(
            row[0]["hash"], old_password
        ):
            return apology("invalid old password", 403)

        # Ensure new passwords match
        if password != confirmation:
            return apology("the passwords don't match", 403)

        # Put new password into db:
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(password), session["user_id"])

        return render_template("success.html")

    else:
        return render_template("settings.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        # validation:
        if not symbol:
            return apology("must provide a symbol")
        stock_info = lookup(request.form.get("symbol"))
        if stock_info is None:
            return apology("incorrect symbol")
        # if provided symbol is OK, give the client stock info:
        return render_template("quoted.html", stock_info=stock_info)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must repeat password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))
            user_row = db.execute("SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = user_row[0]["id"]

            return redirect("/")

        except ValueError:
            return apology("username already exists", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    rows = db.execute("SELECT DISTINCT stock FROM transactions WHERE user_id = ?",
                      session["user_id"])
    stocks = [row["stock"] for row in rows]

    if request.method == "POST":

        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # validate symbol input:
        if not symbol:
            return apology("must provide a symbol")

        # Check symbol input validity:
        if symbol not in stocks:
            return apology("Choose the stock that you posses")

        # Check shares input validity:
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive number of shares")

        shares = int(shares)

        row = db.execute(
            "SELECT SUM(shares) AS total FROM transactions WHERE user_id = ? AND stock = ?",
            session["user_id"], symbol
        )

        curr_shares = row[0]["total"] or 0

        if curr_shares < shares:
            return apology("Not enough shares")

        price = lookup(symbol)["price"]
        revenue = price * shares

        # upd CASH in users tbl
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])
        # add SELL(-shares) transaction into transactions tbl
        db.execute("INSERT INTO transactions (stock, price, shares, user_id) VALUES (?, ?, ?, ?)",
                   symbol, price, -shares, session["user_id"])
        # return render_template("sell.html", stocks=stocks)
        return redirect("/")
    else:

        return render_template("sell.html", stocks=stocks)