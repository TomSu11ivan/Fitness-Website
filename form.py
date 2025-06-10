from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import InputRequired, EqualTo

class RegistationForm(FlaskForm):
    user_id = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("Username:", 
                          validators=[InputRequired()])
    password = PasswordField("Password:",
                             validators=[InputRequired()])
    submit = SubmitField("Submit")

class AdminLoginForm(FlaskForm):
    admin_id = StringField("Username:", 
                           validators=[InputRequired()])
    password = PasswordField("Password:",
                             validators=[InputRequired()])
    submit = SubmitField("Submit")

class FilterForm(FlaskForm):
    filters = RadioField('Price Range', choices=[
        ('<100', 'Less than $100'),
        ('100-200', '$100-$200'),
        ('200-300', '$200-$300'),
        ('300+', 'More than $300')
    ])
    submit = SubmitField('Filter')

class ChangePasswordForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    old_password = PasswordField('Old Password:', validators=[InputRequired()])
    new_password = PasswordField('New Password:', validators=[InputRequired()])
    submit = SubmitField('Change Password')

class CheckoutForm(FlaskForm):
    first_name = StringField("First Name:", validators=[InputRequired()])
    second_name = StringField("Second Name:", validators=[InputRequired()])
    card = IntegerField("Card Number:", validators=[InputRequired()])
    submit = SubmitField('Checkout')