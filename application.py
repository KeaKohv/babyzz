import os
from tempfile import mkdtemp

import psycopg2
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use Heroku PostgreSQL database
db = SQL(os.getenv("DATABASE_URL"))

#For local database
#db = SQL("postgresql://postgres:Kallimaania112@localhost:5432/BabyZz")


@app.route("/")
@login_required
def index():
    """Show index page"""
    first_name = session["first_name"]

    children = children_sleep_needs(session["user_id"])
    return render_template("index.html", first_name=first_name, children=children)


@app.route("/children", methods=["GET", "POST"])
@login_required
def children():
    """Show children's page"""

    # Child was added via the form
    if request.method == "POST":
        
        # Check if name was given
        if not request.form.get("baby_name"):
            return apology("must provide child's name", 403)

        # Check if name contains only strings
        if not all(x.isalpha() or x.isspace() for x in request.form.get("baby_birth")):
            return apology("Child's name can only contain letters", 403)

        # Check if date was given
        if not request.form.get("baby_birth"):
            return apology("must provide child's date of birth", 403)

        # Capitalize the name
        baby_name = request.form.get("baby_name").capitalize()

        # Check if that person already has a child with this name
        rows = db.execute("SELECT * FROM children WHERE parent_id = ?", session["user_id"])
        
        for row in rows:
            if row["baby_name"] == baby_name:
                return apology("You already have a child with this name")
        
        # Add the child to the database
        db.execute("INSERT INTO children (parent_id, baby_name, baby_birth) VALUES (?, ?, ?)",
                   session["user_id"], request.form.get("baby_name"), request.form.get("baby_birth"))
        
        flash("Your child was added")

        # Get children from database
        # children = get_children()
        children = db.execute("SELECT * FROM children WHERE parent_id = ?", session["user_id"])

        return render_template("children.html", children=children)
    else:
        # Get children from database
        children = db.execute("SELECT * FROM children WHERE parent_id = ?", session["user_id"])

        return render_template("children.html", children=children)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Remember username
        session["first_name"] = rows[0]["first_name"]

        # Redirect user to home page
        flash('You were successfully logged in')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""
    if request.method == "POST":
        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("must provide old password", 403)
        # Ensure old password was submitted
        elif not request.form.get("new"):
            return apology("must provide new password", 403)
        # Ensure old password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm new password", 403)
        # Ensure new password and confirmation match
        elif request.form.get("new") != request.form.get("confirmation"):
            return apology("password and its confirmation do not match", 403)

        # Update password in the database
        db.execute("UPDATE users SET hash = :new_hash WHERE id = :user_id",
                   new_hash=generate_password_hash(request.form.get("new")), user_id=session["user_id"])

        return redirect("/")
    if request.method == "GET":
        return render_template("password.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash('You were successfully logged out')
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure first name was submitted
        if not request.form.get("first_name"):
            return apology("must provide first name", 403)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # See if this username already exists in the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("this username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and its confirmation do not match", 400)

        # Insert first name, username and hashed password into database
        db.execute("INSERT INTO users (username, hash, first_name) VALUES (?, ?, ?)",
                   request.form.get("username"),  generate_password_hash(request.form.get("password")),
                   request.form.get("first_name"))

        flash('You were successfully registered')
        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")


def children_sleep_needs(user_id):
    rows = db.execute("SELECT * FROM children WHERE parent_id = ?", user_id)

    children = []
    for row in rows:
        baby_name = row["baby_name"]
        baby_birth = row["baby_birth"]
        baby_age = calculate_age(baby_birth)
        baby_age_in_months = calculate_age_in_months(baby_birth)
        total = "You should have a lot of sleep"
        naps = "Many naps"
        new_child = {
            "baby_name": baby_name,
            "baby_birth": baby_birth,
            "baby_age": baby_age,
            "age_in_months": baby_age_in_months,
            "total": total,
            "naps": naps
        }
        children.append(new_child)

    for child in children:
        months = child["age_in_months"]
        sleep_needs = db.execute("SELECT * FROM sleep_needs WHERE age_min <= ? AND age_max >= ?",
                                  months, months)
       
        if len(sleep_needs) == 1:
            # child["total"] = sleep_needs["total"]
            # child["naps"] = sleep_needs["naps"]
            child["total"] = months
            child["naps"] = "zzz"
        else:
            child["total"] = "zzz"
            child["naps"] = months

    return children


# This function is partly based on the solution given here: https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
def calculate_age(born):
    today = date.today()
    years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    months = today.month - born.month - ((today.day) < (born.day))
    days = today.day - born.day
    
    str_years = "years"
    str_months = "months"
    if years == 1:
        str_years = "year"
    if months == 1:
        str_months = "month"

    if years > 0:
        return f"{years} {str_years} and {months} {str_months}"
    elif months == 0:
        return f"{days} days"
    else:
        return f"{months} {str_months}"

# This function returns age in months
def calculate_age_in_months(born):
    today = date.today()
    years = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    months = today.month - born.month - ((today.day) < (born.day))

    months_total = int(years*12) + int(months)
    
    return months_total
    

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
