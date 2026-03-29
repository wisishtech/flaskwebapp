# app.py - Main Flask Application
# CSC312 - Web Application Development
# This file initialises the Flask app, defines routes, handles form data,
# connects to MySQL, implements password hashing for secure user signup,
# and manages session-based login and logout.

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------------------------
# 1. Initialise Flask Application
# -------------------------------------------------------------------
app = Flask(__name__)

# Secret key is required for flashing messages and session management
app.secret_key = 'csc312_secret_key_2024'

# -------------------------------------------------------------------
# 2. Database Configuration
# Update host, user, password, and database to match your MySQL setup
# -------------------------------------------------------------------
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 8889,
    'user': 'root',
    'password': 'root',        # Your MySQL password
    'database': 'csc312_db',
    'raise_on_warnings': True
}


def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Returns None if the connection fails, allowing graceful error handling.
    Reference: Grinberg (2018) recommends abstracting DB connections
    into helper functions for maintainability.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"[Database Error] Could not connect to MySQL: {e}")
        return None


# -------------------------------------------------------------------
# 3. Homepage Route — also handles the inline login form (POST)
# Renders index.html which contains the hero login form.
# On POST: validates credentials and stores user in session.
# -------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Homepage route supporting GET and POST methods.

    GET  - Renders index.html. If the user is already logged in,
           the template shows a welcome card instead of the login form.

    POST - Handles the login form submitted from the hero section.
           Retrieves username and password from request.form,
           queries tbl_user, and verifies the password using
           check_password_hash(). On success, stores user info
           in Flask's session dictionary.

    Reference: Ronacher (2023) - Flask Documentation.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # --- Form Validation ---
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return redirect(url_for('index'))

        # --- Database Lookup ---
        connection = get_db_connection()
        if connection is None:
            flash('Database error. Please try again later.', 'danger')
            return redirect(url_for('index'))

        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, username, password FROM tbl_user WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()

            # --- Password Verification ---
            # check_password_hash() compares the plain text input against
            # the stored pbkdf2:sha256 hash without ever exposing the original
            # password (Viega & Messier, 2003).
            if user and check_password_hash(user[2], password):
                session['user_id']  = user[0]
                session['username'] = user[1]
                flash(f'Welcome back, {user[1]}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('index'))

        except Error as e:
            print(f"[Login Error] {e}")
            flash('An error occurred during login.', 'danger')
            return redirect(url_for('index'))

        finally:
            cursor.close()
            connection.close()

    # GET request: render the homepage
    return render_template('index.html')


# -------------------------------------------------------------------
# 4. Signup Route
# Handles both GET (display form) and POST (process form) requests.
# Validates input, hashes password, and stores user in the database.
# -------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup route supporting GET and POST methods.

    GET  - Renders the signup form (signup.html).
    POST - Validates form input, hashes the password using Werkzeug's
           generate_password_hash(), and inserts the new user into
           the tbl_user table in MySQL.

    Form validation checks:
      - Username and password fields must not be empty.
      - Password must be at least 6 characters long.

    Password hashing:
      - Uses generate_password_hash() with method='pbkdf2:sha256'
        explicitly set. This is required for Python 3.9 compatibility.
        Newer Werkzeug defaults to 'scrypt' which requires Python 3.10+
        (hashlib.scrypt). Forcing pbkdf2:sha256 ensures the app runs
        correctly on Python 3.8, 3.9, and 3.10+.
      - The plain text password is never stored in the database.
      - Reference: Viega & Messier (2003).
    """
    if request.method == 'POST':
        # Retrieve form data using request.form
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # --- Form Validation ---
        if not username or not password:
            flash('Both username and password are required.', 'danger')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('signup.html')

        # --- Password Hashing ---
        # method='pbkdf2:sha256' explicitly specified to avoid the
        # AttributeError: module 'hashlib' has no attribute 'scrypt'
        # on Python 3.9 where hashlib.scrypt does not exist.
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256'
        )

        # --- Database Insertion ---
        connection = get_db_connection()
        if connection is None:
            flash('Database connection failed. Please try again later.', 'danger')
            return render_template('signup.html')

        try:
            cursor = connection.cursor()

            # Check if username already exists
            cursor.execute(
                "SELECT id FROM tbl_user WHERE username = %s", (username,)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already taken. Please choose another.', 'warning')
                return render_template('signup.html')

            # Insert the new user with hashed password
            cursor.execute(
                "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            connection.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('index'))

        except Error as e:
            print(f"[Database Error] Insert failed: {e}")
            flash('An error occurred while creating your account.', 'danger')
            return render_template('signup.html')

        finally:
            # Always close the cursor and connection to free resources
            cursor.close()
            connection.close()

    # GET request: simply render the signup form
    return render_template('signup.html')


# -------------------------------------------------------------------
# 5. Logout Route
# Clears the session and redirects the user to the homepage.
# -------------------------------------------------------------------
@app.route('/logout')
def logout():
    """
    Logout route. Calls session.clear() to remove all session data,
    effectively signing the user out. A flash message confirms the
    action before redirecting to the homepage.
    Reference: Grinberg (2018).
    """
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# -------------------------------------------------------------------
# 6. Run the Application
# debug=True enables auto-reload and detailed error messages during
# development. Set to False in production.
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)