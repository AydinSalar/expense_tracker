from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, DateField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length

# Registration Form
class RegistrationForm(FlaskForm):
    # Fields for user registration
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=2, max=20, message="Username must be between 2 and 20 characters.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Register')

    # Custom validation to check if the username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')

    # Custom validation to check if the email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

# Login Form
class LoginForm(FlaskForm):
    # Fields for user login
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Option to remember the user
    submit = SubmitField('Login')

# Expense Form
class ExpenseForm(FlaskForm):
    # Fields for adding/editing an expense
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.01, message="Amount must be greater than 0.")
    ])
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    description = TextAreaField('Description')  # Optional field for description
    submit = SubmitField('Submit')
