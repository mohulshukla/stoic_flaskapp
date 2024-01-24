import os
import requests
import urllib.parse
import sqlite3

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('quotes_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_random_quote():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')
    quote = cursor.fetchone()
    conn.close()
    return quote