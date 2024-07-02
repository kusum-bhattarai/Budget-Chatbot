import random
from .app import User, Expense
from . import db

class BudgetChatbot:
    def __init__(self, user_id):
        self.user_id=user_id
        self.user=User.query.get(user_id)
        if not self.user:
            self.user=User(id=user_id)
            db.session.add(self.user)
            db.session.commit()

    def add_expense(self, amount):
        expense=Expense(amount=amount, user_id=self.user_id)
        db.session.add(expense)
        db.session.commit()
        return f"Added an expense of {amount}."
    
    def set_budget(self, amount):
        self.user.budget=amount
        db.session.commit()
        return f"Set your budget to {amount}."
    
    def provide_advice(self):
        total_expenses=sum(expense.amount for expense in self.user.expenses)
        if total_expenses>self.user.budget:
            return "You have exceeded your budget. Consider reducing unnecessary expenses."
        return "You are within your budget. Great!"
    
    def shopping_advice(self):
        tips=[
            "You don't need too many clothes.",
            "You have more than enough clothes. Try making outfits from them first."
            "Wait for the right time."
            "Don't be impulsive!"
        ]
        return random.choice(tips)
    
    def handle_message(self, message):
        message=message.lower()
        if "hello" in message or "hi" in message:
            return "Hello! How can I assist you with your budget today?"
        
        elif "budget" in message:
            return self.provide_advice()
        
        elif "advice" in message or "tips" in message:
            return self.shopping_advice()
        
        elif "expense" in message and "add" in message:
            try:
                amount=float(message.split()[-1])
                return self.add_expense(amount)
            except ValueError:
                return "Please provide a valid expense amount."
        
        elif "set budget" in message:
            try:
                amount=float(message.split()[-1])
                return self.set_budget(amount)
            except ValueError:
                return "Please provide a valid budget amount."
            
        elif "reduce shopping" in message or "save money" in message:
            return self.shopping_advice()
        
        else:
            return "I am not sure how to respond to that. You can ask me anything about your budget and finances."
            
      

   