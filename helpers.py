import os
import requests
import urllib.parse
import sqlite3

from flask import redirect, render_template, request, session, jsonify
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


# Generate Quote from API Helper Functions

def retrieve():
    try:
        response = requests.get('https://stoic-quotes.com/api/quote')
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException:
        return jsonify(error="Error fetching quote from API"), 500

    quote_data = response.json()
    print(quote_data)
    return quote_data

def get_saved_quotes():
    connection = sqlite3.connect('quotes_app.db')
    cursor = connection.cursor()
    
    user_id = session['user_id']

    cursor.execute("SELECT quote_text, author FROM quotes WHERE user_id = ?", (user_id,))
    quotes = cursor.fetchall()

    connection.close()
    print(quotes)
    return quotes
