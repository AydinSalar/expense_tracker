from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db, Expense
from forms import RegistrationForm, LoginForm, ExpenseForm
from werkzeug.security import generate_password_hash, check_password_hash

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect authenticated users to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password and create a new user
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect authenticated users to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Query user by email
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route for displaying and paginating user's expenses
@app.route('/expenses')
@login_required
def expenses():
    page = request.args.get('page', 1, type=int)
    # Query expenses by the current user, ordered by date in descending order
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).paginate(page=page, per_page=10)
    return render_template('expenses.html', expenses=expenses)

# Route for adding a new expense
@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        # Create new expense linked to the current user
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
        return redirect(url_for('expenses'))
    return render_template('add_expense.html', form=form)

# Route for editing an existing expense
@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    # Query the expense by ID, or return a 404 error if not found
    expense = Expense.query.get_or_404(expense_id)
    # Ensure the current user is the owner of the expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense.', 'danger')
        return redirect(url_for('expenses'))
    
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        # Update expense details
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.date = form.date.data
        expense.description = form.description.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses'))
    return render_template('edit_expense.html', form=form)

# Route for deleting an expense
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    # Query the expense by ID, or return a 404 error if not found
    expense = Expense.query.get_or_404(expense_id)
    # Ensure the current user is the owner of the expense
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('expenses'))
    
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses'))
