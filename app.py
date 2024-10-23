from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Expense  # Import db from models.py
from forms import RegistrationForm, LoginForm, ExpenseForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database with Flask app
db.init_app(app)

# Create database tables
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created.")

# Set up database migration tool
migrate = Migrate(app, db)

# Set up CSRF protection
csrf = CSRFProtect(app)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up logging for error tracking
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/expense_tracker.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

# Load user by ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Edit existing expense
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    # Ensure current user is the owner of the expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense.', 'danger')
        return redirect(url_for('expenses'))
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.date = form.date.data
        expense.description = form.description.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses'))
    return render_template('edit_expense.html', form=form, expense=expense)

# Delete an expense
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    # Ensure current user is the owner of the expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses'))

# View all expenses for current user
@app.route('/expenses')
@login_required
def expenses():
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).paginate(page=page, per_page=10)
    return render_template('expenses.html', expenses=expenses)

# Add a new expense
@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    try:
        if form.validate_on_submit():
            expense = Expense(
                amount=form.amount.data,
                category=form.category.data,
                date=form.date.data,
                description=form.description.data,
                user_id=current_user.id
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding expense: {e}')
        flash('An error occurred while adding the expense.', 'danger')
    return render_template('add_expense.html', form=form)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

# User dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    # Total expenses
    total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0.00

    # Expenses by Category
    expenses_by_category = (
        db.session.query(Expense.category, db.func.sum(Expense.amount))
        .filter_by(user_id=current_user.id)
        .group_by(Expense.category)
        .all()
    )

    # Expenses by Month (Last 6 Months)
    from datetime import datetime, timedelta
    six_months_ago = datetime.now() - timedelta(days=180)
    expenses_by_month = (
        db.session.query(
            db.func.strftime('%Y-%m', Expense.date).label('month'),
            db.func.sum(Expense.amount).label('total')
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.date >= six_months_ago
        )
        .group_by('month')
        .order_by('month')
        .all()
    )

    # Prepare data for Chart.js
    category_labels = [row[0] for row in expenses_by_category]
    category_values = [float(row[1]) for row in expenses_by_category]
    month_labels = [row[0] for row in expenses_by_month]
    month_values = [float(row[1]) for row in expenses_by_month]

    return render_template(
        'dashboard.html',
        total_expenses=total_expenses,
        category_labels=category_labels,
        category_values=category_values,
        month_labels=month_labels,
        month_values=month_values
    )

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors and log them
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f'Server Error: {e}, Route: {request.url}')
    return render_template('500.html'), 500

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)
