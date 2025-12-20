import os
import json
from datetime import datetime

from helpers import login_required, apology
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt
import sqlite3

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration
DATABASE = 'miko.db'


# Function to connect to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name
    return conn


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
# @login_required
def index():
    """Home page"""
    session["csrf"] = gen_salt(32)

    return render_template("index.html", miko_csrf=session["csrf"])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            flash("meowwww")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")

        # Query database for username
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()

        # Ensure username exists and password is correct
        if user is None:
            flash("User not found")
            return redirect("/login")
        
        if not check_password_hash(user["hash"], request.form.get("password")):
            flash("Incorrect Password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = user["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", messages=get_flashed_messages())


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()  # Forget any user_id
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # Validate input
        if not email or not username or not password or not confirm:
            flash("Field left empty")
            return redirect("/register")

        if password != confirm:
            flash("Passwords do not match")
            return redirect("/register")

        # Hash password and store user in database
        hash = generate_password_hash(password)
        db = get_db()

        try:
            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", (username, hash, email))
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username/email already taken")
            return redirect("/register")

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
        return redirect("/")

    else:
        return render_template("register.html", messages=get_flashed_messages())


@app.route("/submit", methods=["POST"])
def submit():
    csrf = request.form.get("csrf")
    if not csrf or "csrf" not in session or csrf != session["csrf"]:
        return jsonify({"error": "CSRF NOT VALID"}), 403
    
    if "user_id" not in session:
        return jsonify({"abort": "User Not Logged In"}), 200
    

    score = request.form.get("score")
    solved = request.form.get("solved")
    total = request.form.get("total")
    difficulty = request.form.get("difficulty")
    time_taken = request.form.get("time")
    timestamp = request.form.get("timestamp")
    user_id = session["user_id"]

    score = float(score)
    solved = int(solved)
    total = int(total)
    time_taken = float(time_taken)
    timestamp = int(timestamp) // 1000
    print(timestamp)
    difficulty = difficulty.lower()

    db = get_db();
    cursor = db.execute(
        "INSERT INTO scores (user_id, score, time_used, solved, total, difficulty, timestamp)\
        VALUES (?, ?, ?, ?, ?, ?, datetime(?, 'unixepoch'))", (
            user_id, score, time_taken, solved, 
            total, difficulty, timestamp
        )
    )

    score_id = cursor.lastrowid;

    cursor = db.execute(
        "SELECT score FROM leaderboard WHERE user_id = ? AND difficulty = ?",
        (user_id, difficulty)
    )

    row = cursor.fetchone()

    if not row:
        db.execute(
            "INSERT INTO leaderboard (user_id, score_id, difficulty, score)\
            VALUES (?, ?, ?, ?)", (
                user_id, score_id, difficulty, score
            )
        )
    elif row["score"] < score:
        db.execute(
            "UPDATE leaderboard SET score_id = ?, score = ? \
            WHERE user_id = ? AND difficulty = ?", (
                score_id, score, user_id, difficulty
            )
        )

    db.commit()

    return jsonify({"success": "Score stored"}), 201


@app.route("/leaderboard")
def leaderboard():
    difficulty = request.args.get("difficulty")

    if not difficulty or difficulty.lower() not in ["medium", "hard"]:
        difficulty = "easy"
    else:
        difficulty = difficulty.lower()

    db = get_db()
    cursor = db.execute(
        """SELECT u.username, l.score
        FROM leaderboard l
        JOIN users u ON l.user_id = u.id
        WHERE l.difficulty = ?
        ORDER BY l.score DESC
        LIMIT 20""", (difficulty,)
    )

    leaderboard = cursor.fetchall()

    return render_template("leaderboard.html", difficulty=difficulty, leaderboard=leaderboard)


@app.route("/profile")
@login_required
def profile():
    pass


@app.route("/history")
@login_required
def history():
    user_id = session.get("user_id")
    db = get_db()
    cursor = db.execute("SELECT * FROM scores WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))

    data = cursor.fetchall()
    return render_template("history.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
