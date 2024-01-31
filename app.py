from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
from flask_session import Session
from cs50 import SQL
import random
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, get_saved_quotes, get_sorted_quotes
import requests

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quotes_app.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response





# default (view saved quotes) route
@app.route('/')
@login_required
def index():
    quotes = get_saved_quotes()
    return render_template('index.html', quotes=quotes)



# login route
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

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


#  logout route
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Validate submission
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure password == confirmation
        if not (password == confirmation):
            return apology("the passwords do not match", 400)

        # Ensure password not blank
        if password == "" or confirmation == "" or username == "":
            return apology("input is blank", 400)

        # Ensure username does not exists already
        if len(rows) == 1:
            return apology("username already exist", 400)
        else:
            hashcode = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashcode)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")




# generate quote route
@app.route('/generate')
@login_required
def generate():
    try:
        response = requests.get('https://stoic-quotes.com/api/quote')
        response.raise_for_status()
        data = response.json()
        quote_text = data.get('text')  # Extract quote text
        quote_author = data.get('author')  # Extract quote author
        print(quote_text, quote_author)
    except requests.RequestException as e:
        print(e)
        return apology("Could not Fetch Quote From API", 403)

    # Pass the quote text and author separately to the template
    return render_template('generate.html', quote_text=quote_text, quote_author=quote_author)


# saving quote route
@app.route('/save', methods=['POST'])
@login_required
def save_quote():
    quote_text = request.form.get('quote_text')
    quote_author = request.form.get('quote_author')
    user_id = session.get('user_id')  # Since user is already logged in
    
    # Save quote to the database
    connection = sqlite3.connect('quotes_app.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO quotes (quote_text, author, user_id) VALUES (?, ?, ?)
    ''', (quote_text, quote_author, user_id))
    
    connection.commit()
    connection.close()
    flash('Quote added successfully!')
    # Redirect to a new page or the same page with a success message
    return redirect(url_for('generate'))  # Redirect back to the generate route or to a 'success' route



# deleting route
@app.route('/delete/<quote_text>')
@login_required
def delete_quote(quote_text):
    user_id = session.get('user_id')
    connection = sqlite3.connect('quotes_app.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM quotes WHERE quote_text = ? AND user_id = ?", (quote_text, user_id))
    connection.commit()
    connection.close()
    
    flash('Quote deleted successfully')
    return redirect(url_for('index'))


# add quote route
@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    ''' Add quote and its author manually '''
    if request.method == 'POST':
        quote_text = request.form.get('quote')
        author = request.form.get('author')

        if not quote_text or not author:
            # Handle the case where quote or author is empty
            return redirect(url_for('add_quote'))

        # Assuming 'user_id' is stored in the session upon login
        user_id = session.get('user_id')

        connection = sqlite3.connect('quotes_app.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO quotes (quote_text, author, user_id) VALUES (?, ?, ?)", (quote_text, author, user_id))

        connection.commit()
        connection.close()
        flash('Quote added successfully!')

        return redirect(url_for('index'))

    return render_template('add.html')


# share quote route
@app.route('/share')
@login_required
def share():
    sort_method = request.args.get('sort', 'last_added')
    quotes = get_sorted_quotes(sort_method)
    return render_template('share.html', quotes=quotes, current_sort_method=sort_method)


# mystery route
@app.route('/mystery')
@login_required
def mystery():
    pass


if __name__ == '__main__':
    app.run(debug=True)
    