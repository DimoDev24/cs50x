import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

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
    """Show portfolio of stocks"""
    uid = session["user_id"]
    rows = db.execute(
        """
        SELECT symbol, SUM(number) AS shares
        FROM history
        WHERE uid = ?
        GROUP BY symbol
        HAVING SUM(number) > 0
        """,
        uid
    )

    for row in rows:
        quote = lookup(row["symbol"])
        if quote is None:
            return apology("invalid symbol", 400)

        row["price"] = quote["price"]
        row["total"] = row["shares"] * row["price"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", uid)[0]["cash"]

    return render_template("index.html", portfolio=rows, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if len(symbol) < 6 and symbol.isalpha():
            if not symbol:
                return apology("Symbol cannot be blank.")
            shares = request.form.get("shares")

            try:
                shares = int(shares)

            except ValueError:
                return apology("Cannot put letters or symbols.")

            if shares < 1:
                return apology("Cannot buy 0 or negative number of shares.")

            quote = lookup(symbol)
            if quote is None:
                return apology("invalid symbol", 400)

            cost = (quote["price"] * shares)

            uid = session["user_id"]

            result = db.execute("SELECT cash FROM users WHERE id = ?", uid)
            money = float(result[0]["cash"])

            now = datetime.now()
            now = now.replace(microsecond=0)

            if money < cost:
                return apology("You dont have enough cash...")

            db.execute("INSERT INTO history (symbol, number, amount, action, uid, datetime) VALUES (?, ?, ?, ?, ?, ?)",
                    symbol, shares, cost, "BOUGHT", uid, now)

            money = (money - cost)
            db.execute("UPDATE users SET cash = (?) WHERE id = (?)", money, uid)

            return redirect("/")

        else:
            return apology("Invalid symbol format.")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    uid = session["user_id"]
    rows = db.execute(
        """
        SELECT symbol, number, amount, action, datetime
        FROM history
        WHERE uid = ?
        """,
        uid
    )

    return render_template("history.html", rows=rows)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Show history of transactions"""
    uid = session["user_id"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", uid)
    cash = float(cash[0]["cash"])

    if request.method == "POST":
        number = request.form.get("number")
        if not number:
            return apology("You need to put a number of cash.")

        try:
            number = int(number)

        except ValueError:
            return apology("Cannot put letters or symbols.")

        money = cash + number

        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", money, uid)

        return redirect("/")

    else:
        return render_template("addcash.html", cash=cash)


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
        if len(symbol) == 4 and symbol.isalpha():
            if not symbol:
                return apology("Must provide a symbol.")

            quote = lookup(symbol)

            stock={"name": quote["name"],
                "symbol": quote["symbol"],
                "price": usd(quote["price"])}

            return render_template("quoted.html", name=stock["name"], symbol=stock["symbol"], price=stock["price"])

        else:
            return apology("Invalid symbol format.")

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Must provide an username.")

        password = request.form.get("password")
        if not password:
            return apology("Must provide a password.")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("The password confirmation doesn't match.")

        passhash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passhash)

        except:
            return apology("The username is already taken...")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    rows = db.execute(
        "SELECT symbol, SUM(number) AS shares FROM history WHERE uid = ? GROUP BY symbol",
        session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must select a symbol.")

        shares = request.form.get("shares")

        try:
            shares = int(shares)

        except ValueError:
            return apology("Cannot put letters or symbols.")

        owned = 0
        for row in rows:
            if row["symbol"] == symbol:
                owned = row["shares"]
                break

        if shares > owned:
            return apology("You don't own that many shares")
        if not shares:
            return apology("Must select number of shares.")

        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol", 400)

        uid = session["user_id"]

        cash = db.execute("SELECT cash FROM users WHERE id = ?", uid)
        money = float(cash[0]["cash"])
        amount = money + (quote["price"] * shares)

        now = datetime.now()
        now = now.replace(microsecond=0)

        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", amount, uid)

        db.execute(
            "INSERT INTO history (symbol, number, amount, action, uid, datetime) VALUES (?, ?, ?, ?, ?, ?)",
            symbol,
            -shares,
            quote["price"],
            "SELL",
            uid,
            now
        )

        return redirect("/")

    return render_template("sell.html", portfolio=rows)
