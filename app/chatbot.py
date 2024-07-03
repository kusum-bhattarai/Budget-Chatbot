from .app import User, Expense
from . import db
import random

class BudgetChatbot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.query.get(user_id)
        if not self.user:
            self.user = User(id=user_id)
            db.session.add(self.user)
            db.session.commit()

    def add_expense(self, name, amount):
        expense = Expense(name=name, amount=amount, user_id=self.user_id)
        db.session.add(expense)
        db.session.commit()
        return f"Added an expense of {amount} for {name}."

    def set_budget(self, amount):
        self.user.budget = amount
        db.session.commit()
        return f"Set your budget to {amount}."

    def set_savings_goal(self, amount):
        self.user.savings_goal = amount
        db.session.commit()
        return f"Set your savings goal to {amount}."

    def provide_advice(self):
        total_expenses = sum(expense.amount for expense in self.user.expenses)
        if total_expenses > self.user.budget:
            return "You have exceeded your budget. Consider reducing unnecessary expenses."
        return "You are within your budget. Keep it up!"

    def shopping_advice(self):
        tips = [
            "Make a shopping list and stick to it.",
            "Avoid shopping when you are hungry.",
            "Look for discounts and coupons.",
            "Consider buying in bulk for items you use frequently.",
            "Avoid impulse purchases by waiting 24 hours before buying non-essential items."
        ]
        return random.choice(tips)

    def handle_message(self, message):
        message = message.lower()
        if "hello" in message or "hi" in message:
            return "Hello! How can I assist you with your budget today?"
        elif "budget" in message:
            return self.provide_advice()
        elif "advice" in message or "tips" in message:
            return self.shopping_advice()
        elif "expense" in message and "add" in message:
            try:
                parts = message.split()
                name = parts[2]
                amount = float(parts[3])
                return self.add_expense(name, amount)
            except ValueError:
                return "Please provide a valid expense amount."
        elif "set budget" in message:
            try:
                amount = float(message.split()[-1])
                return self.set_budget(amount)
            except ValueError:
                return "Please provide a valid budget amount."
        elif "set savings goal" in message:
            try:
                amount = float(message.split()[-1])
                return self.set_savings_goal(amount)
            except ValueError:
                return "Please provide a valid savings goal amount."
        elif "reduce spending" in message or "save money" in message:
            return self.shopping_advice()
        else:
            return "I'm not sure how to respond to that. You can ask me about your budget, add expenses, set budget or savings goal, or ask for advice on saving money."
