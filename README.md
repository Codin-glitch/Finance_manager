#  Personal Finance Manager (CLI) – Django Project

A Command-Line Interface (CLI) application built using Django to help users manage their income, expenses, budgeting, and generate financial reports. All features work from the command line, making it ideal for terminal-based usage.

---

##  Features

-  User Registration, Login, and Logout with session management
-  Add, View, Edit, and Delete Transactions
-  View category-wise income and expense summaries
-  Generate Monthly and Yearly Reports
-  Set and Check Budgets per category
-  Backup all user data to a JSON file and restore when needed.

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/Codin-glitch/Finance_management.git
cd finance_manager
```

### 2. Create and activate a virtual environment

```bash
python -m venv .finance
.finance\Scripts\activate  # Windows
# OR
source .finance/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

##  Usage

All commands are run using the Django `manage.py` CLI.

###  User Authentication

```bash
python manage.py register_user       # Register a new user
python manage.py login_user          # Login to start a session
python manage.py logout_user         # Logout and clear session
```

###  Transaction Management

```bash
python manage.py add_transaction         # Add a new transaction
python manage.py view_transactions       # View all transactions
    --type=income|expense                # Optional filter
    --category=<CategoryName>            # Optional filter

python manage.py edit_transaction --id=1 # Edit a transaction by ID
python manage.py delete_transaction      # Delete a transaction by ID
python manage.py category_summary        # Summary by category
```

###  Budget and Reports

```bash
python manage.py set_budget              # Set a monthly category budget
python manage.py check_budget --category=Food  # Check current spending vs. budget
python manage.py monthly_report          # View monthly financial summary
python manage.py yearly_report           # View yearly financial summary
python manage.py backup_data             # Export all user data as JSON
python managw.py restore_data            # Restores the data using backup.json
```

---

##  Running Tests

To run all unit tests:

```bash
python manage.py test
```

Or to test specific apps:

```bash
python manage.py test users
python manage.py test tracker
```

---

##  Notes

- All user session information is stored in a local `session.txt` file.
- The app uses SQLite by default, but you can configure any database via `settings.py`.
- `backup_data` creates a `backup.json` file containing all user and transaction info.

---

##  Author

Made by Codin-glitch

---
