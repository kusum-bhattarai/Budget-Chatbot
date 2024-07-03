from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from . import db
from .app import User, Expense
from .forms import RegistrationForm, LoginForm, ExpenseForm, UpdateExpenseForm
from .chatbot import get_chatbot_response
from . import create_app, login_manager

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(name=form.name.data, amount=form.amount.data, type=form.type.data, user=current_user)
        db.session.add(expense)
        if form.type.data == 'bank':
            current_user.current_balance -= form.amount.data
        elif form.type.data == 'credit':
            current_user.credit_balance += form.amount.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    expenses = Expense.query.filter_by(user=current_user)
    remaining_to_goal = current_user.savings_goal - current_user.current_balance
    return render_template('dashboard.html', form=form, expenses=expenses, remaining_to_goal=remaining_to_goal)

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)
    form = UpdateExpenseForm()
    if form.validate_on_submit():
        expense.name = form.name.data
        expense.amount = form.amount.data
        expense.type = form.type.data
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.name.data = expense.name
        form.amount.data = expense.amount
        form.type.data = expense.type
    return render_template('edit_expense.html', form=form)

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    response = get_chatbot_response(data['message'], current_user)
    return {'response': response}

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    response = get_chatbot_response(data['message'], current_user)
    return {'response': response}

