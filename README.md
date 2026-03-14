# Student Budget Expense Tracker

A full-stack web application built with Django to help students manage their income,
track daily expenses, categorize spending, and monitor their monthly budget.

# Features

- ✅ User Registration & Login
- ✅ Dashboard with income, expenses and remaining balance
- ✅ Add and delete income entries
- ✅ Add and delete expenses with categories
- ✅ Monthly transaction list with filters
- ✅ Expense categories management
- ✅ Monthly report with bar and doughnut charts
- ✅ Responsive design with clean sidebar navigation
- ✅ Django admin panel

# Tech Stack

| Layer        | Technology                          |
|--------------|--------------------------------------|
| Backend      | Django 5.0                          |
| Database     | PostgreSQL hosted on Neon           |
| DB Driver    | psycopg2-binary                     |
| Frontend     | HTML, CSS, JavaScript, Chart.js     |
| Auth         | Django built-in authentication      |
| Environment  | python-dotenv                       |

---

# Project Structure
```
sbt/
│
├── config/                        # Django project configuration
│   ├── settings.py                # Settings + Neon DB connection
│   ├── urls.py                    # Root URL dispatcher
│   └── wsgi.py
│
├── accounts/                      # User authentication app
│   ├── forms.py                   # RegisterForm
│   ├── views.py                   # register, login, logout
│   ├── urls.py
│   └── templates/accounts/
│       ├── login.html
│       └── register.html
│
├── expenses/                      # Core budget app
│   ├── models.py                  # Category, Income, Expense
│   ├── forms.py                   # IncomeForm, ExpenseForm, CategoryForm
│   ├── views.py                   # All views
│   ├── urls.py
│   ├── utils.py                   # Budget calculation helpers
│   └── templates/expenses/
│       ├── dashboard.html
│       ├── add_income.html
│       ├── add_expense.html
│       ├── expense_list.html
│       ├── categories.html
│       └── report.html
│
├── templates/
│   └── base.html                  # Global layout with sidebar
│
├── static/
│   ├── css/style.css              # Complete design system
│   └── js/
│       ├── main.js                # Global JS utilities
│       └── report.js              # Chart.js charts
│
├── manage.py
├── requirements.txt
├── .env                           # Environment variables (not committed)
└── .gitignore

Installation & Setup
#1. Clone the repository
git clone https://github.com/YOUR_USERNAME/student-budget-tracker.git
cd student-budget-tracker

### 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

### 4. Set up environment variables
Create a `.env` file in the project root:
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

Generate a SECRET_KEY:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 5. Run migrations
```bash
python manage.py makemigrations expenses
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
Visit: http://127.0.0.1:8000

# Database Setup (Neon PostgreSQL)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Go to **Connection Details** and copy the connection string
4. Paste it into your `.env` as `DATABASE_URL`
5. Run `python manage.py migrate`

# Database Models
auth_user          (Django built-in)
│
├── Category       name, user (FK)
├── Income         amount, source, date, user (FK)
└── Expense        amount, description, date, user (FK), category (FK)

# Business Logic
Remaining Balance = Total Income − Total Expenses

All calculations are scoped to the logged-in user and filtered
by the current month and year by default.

# Security
- All views protected with `@login_required`
- CSRF protection on every form
- Passwords hashed with Django's PBKDF2
- Credentials stored in `.env` (never committed)
- Neon connection uses `sslmode=require`

# App Pages
| Page                | URL                    |
|---------------------|------------------------|
| Login               | `/accounts/login/`     |
| Register            | `/accounts/register/`  |
| Dashboard           | `/dashboard/`          |
| Add Income          | `/income/add/`         |
| Add Expense         | `/expenses/add/`       |
| Transaction List    | `/expenses/`           |
| Categories          | `/categories/`         |
| Monthly Report      | `/report/`             |
| Django Admin        | `/admin/`              |


# Deployment

For production deployment:
1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Run `python manage.py collectstatic`
4. Deploy on **Railway**, **Render**, or **PythonAnywhere**

# Future Improvements

- [ ] Edit expense and income entries
- [ ] Budget limit per category with alerts
- [ ] Export transactions to CSV
- [ ] User profile page
- [ ] Search and filter expenses
- [ ] Pagination on transaction list
- [ ] Email notifications for budget limits

Built with Django as a student budget management project.
