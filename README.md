# CSC312 Flask Web Application
**MIVA Open University | Web Application Development | 2024**

A secure, session-based Flask web application demonstrating user registration, login, password hashing, and MySQL database integration.

---

## Features

- Homepage with an inline login form in the hero section
- Avatar dropdown in the navbar showing the logged-in username with a logout option
- User signup with server-side form validation
- Password hashing using `pbkdf2:sha256` (Werkzeug) — compatible with Python 3.9+
- MySQL database integration via `mysql-connector-python`
- Session-based authentication with Flask's `session` object
- Flash messages for user feedback on all actions
- Fully responsive layout using Bootstrap 5

---

## Project Structure

```
flask_app/
    app.py                  # Flask backend (routes, login, signup, logout)
    requirements.txt        # Python dependencies
    create_table.sql        # MySQL database and table setup script
    README.md               # This file
    templates/
        index.html          # Homepage with login form and avatar dropdown
        signup.html         # Registration page with password strength meter
```

---

## Requirements

- Python 3.9 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

---

## Setup Instructions

### 1. Clone or download the project

Place all files in a folder named `flask_app/`.

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the MySQL database

Open MySQL Workbench or the MySQL terminal and run:

```bash
mysql -u root -p < create_table.sql
```

Or manually paste the contents of `create_table.sql` into MySQL Workbench and execute it.

### 5. Configure your database credentials

Open `app.py` and update the `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # update this
    'database': 'csc312_db'
}
```

### 6. Run the application

```bash
python app.py
```

The app will start at: **http://127.0.0.1:5000**

---

## Usage

| Page | URL | Description |
|------|-----|-------------|
| Homepage | `/` | Login form in hero section. Shows welcome card when logged in. |
| Sign Up | `/signup` | Register a new account with password hashing. |
| Logout | `/logout` | Clears session and redirects to homepage. |

---

## Important Notes

### Python 3.9 Compatibility Fix
Newer versions of Werkzeug default to `scrypt` for password hashing, which requires Python 3.10+. This project explicitly uses `pbkdf2:sha256` to ensure compatibility with Python 3.9:

```python
# Correct (works on Python 3.9+):
generate_password_hash(password, method='pbkdf2:sha256')

# Do NOT use (breaks on Python 3.9):
generate_password_hash(password)
```

### Security Reminders
- Never commit your real database password to a public repository.
- Set `debug=False` before deploying to production.
- Change `app.secret_key` to a long, random string in production.

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.3 | Web framework and routing |
| mysql-connector-python | 8.4.0 | MySQL database driver |
| Werkzeug | 3.0.3 | Password hashing utilities |

---

## References

- Grinberg, M. (2018). *Flask web development* (2nd ed.). O'Reilly Media.
- Oracle Corporation. (2023). *MySQL connector/Python developer guide*. https://dev.mysql.com/doc/connector-python/en/
- Otto, M., & Thornton, J. (2023). *Bootstrap 5 documentation*. https://getbootstrap.com/docs/5.3/
- OWASP. (2023). *Password storage cheat sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Ronacher, A. (2023). *Flask documentation (v3.0)*. https://flask.palletsprojects.com/
- Viega, J., & Messier, M. (2003). *Secure programming cookbook for C and C++*. O'Reilly Media.