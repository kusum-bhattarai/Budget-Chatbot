from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .app import User, Expense
from .chatbot import BudgetChatbot
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('main.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.dashboard'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash('Invalid username or password.')
        return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    total_expenses = sum(expense.amount for expense in current_user.expenses)
    remaining_budget = current_user.budget - total_expenses
    savings_needed = current_user.savings_goal - remaining_budget
    return render_template(
        'dashboard.html',
        budget=current_user.budget,
        savings_goal=current_user.savings_goal,
        current_savings=remaining_budget,
        remaining_to_goal=savings_needed,
        expenses=current_user.expenses
    )

@main.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    message = data.get('message')
    chatbot = BudgetChatbot(current_user.id)
    response = chatbot.handle_message(message)
    return jsonify({'response': response})
