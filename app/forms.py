from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    name = StringField('Expense Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    type = StringField('Type (bank/credit)', validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class UpdateExpenseForm(FlaskForm):
    name = StringField('Expense Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    type = StringField('Type (bank/credit)', validators=[DataRequired()])
    submit = SubmitField('Update Expense')
