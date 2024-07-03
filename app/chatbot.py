from .models import Expense, User
from . import db

def get_chatbot_response(message, user):
    responses = {
        "greeting": ["Hello! How can I assist you today?", "Hi there! Need any help with your budget?"],
        "advice": [
            "It's always good to save a portion of your income.",
            "Try to keep track of your expenses daily.",
            "Consider setting aside money for emergencies.",
            "Review your budget regularly and adjust as needed.",
            "Pay off high-interest debt first to save money on interest."
        ],
        "expense_add": ["You can add an expense by specifying the name, amount, and type (bank/credit)."],
        "expense_edit": ["You can edit an expense by specifying the name, amount, and type (bank/credit)."],
        "expense_delete": ["You can delete an expense by providing the expense ID."],
        "budget_update": ["You can update your budget by specifying the new budget amount."],
        "savings_goal_update": ["You can update your savings goal by specifying the new goal amount."],
        "default": ["Sorry, I didn't understand that. Can you rephrase?"]
    }

    message_lower = message.lower()

    if "hello" in message_lower or "hi" in message_lower:
        return random.choice(responses["greeting"])
    elif "advice" in message_lower:
        return random.choice(responses["advice"])
    elif "add expense" in message_lower:
        return add_expense(message_lower, user)
    elif "edit expense" in message_lower:
        return edit_expense(message_lower, user)
    elif "delete expense" in message_lower:
        return delete_expense(message_lower, user)
    elif "update budget" in message_lower:
        return update_budget(message_lower, user)
    elif "update savings goal" in message_lower:
        return update_savings_goal(message_lower, user)
    else:
        return random.choice(responses["default"])

def add_expense(message, user):
    try:
        parts = message.split()
        name = parts[parts.index("name") + 1]
        amount = float(parts[parts.index("amount") + 1])
        expense_type = parts[parts.index("type") + 1]
        
        if expense_type not in ["bank", "credit"]:
            return "Invalid expense type. Please specify 'bank' or 'credit'."

        expense = Expense(name=name, amount=amount, type=expense_type, user=user)
        db.session.add(expense)
        
        if expense_type == "bank":
            user.current_balance -= amount
        elif expense_type == "credit":
            user.credit_balance += amount

        db.session.commit()
        return f"Expense '{name}' added successfully."
    except Exception as e:
        return str(e)

def edit_expense(message, user):
    try:
        parts = message.split()
        expense_id = int(parts[parts.index("id") + 1])
        expense = Expense.query.get(expense_id)
        
        if not expense or expense.user != user:
            return "Expense not found or you do not have permission to edit this expense."
        
        if "name" in parts:
            expense.name = parts[parts.index("name") + 1]
        if "amount" in parts:
            amount_diff = float(parts[parts.index("amount") + 1]) - expense.amount
            if expense.type == "bank":
                user.current_balance -= amount_diff
            elif expense.type == "credit":
                user.credit_balance += amount_diff
            expense.amount = float(parts[parts.index("amount") + 1])
        if "type" in parts:
            new_type = parts[parts.index("type") + 1]
            if new_type not in ["bank", "credit"]:
                return "Invalid expense type. Please specify 'bank' or 'credit'."
            if expense.type != new_type:
                if new_type == "bank":
                    user.current_balance -= expense.amount
                    user.credit_balance -= expense.amount
                elif new_type == "credit":
                    user.credit_balance += expense.amount
                    user.current_balance += expense.amount
                expense.type = new_type
        
        db.session.commit()
        return f"Expense '{expense.name}' updated successfully."
    except Exception as e:
        return str(e)

def delete_expense(message, user):
    try:
        parts = message.split()
        expense_id = int(parts[parts.index("id") + 1])
        expense = Expense.query.get(expense_id)
        
        if not expense or expense.user != user:
            return "Expense not found or you do not have permission to delete this expense."

        if expense.type == "bank":
            user.current_balance += expense.amount
        elif expense.type == "credit":
            user.credit_balance -= expense.amount

        db.session.delete(expense)
        db.session.commit()
        return f"Expense '{expense.name}' deleted successfully."
    except Exception as e:
        return str(e)

def update_budget(message, user):
    try:
        parts = message.split()
        new_budget = float(parts[parts.index("budget") + 1])
        user.budget = new_budget
        db.session.commit()
        return f"Budget updated to {new_budget}."
    except Exception as e:
        return str(e)

def update_savings_goal(message, user):
    try:
        parts = message.split()
        new_goal = float(parts[parts.index("goal") + 1])
        user.savings_goal = new_goal
        db.session.commit()
        return f"Savings goal updated to {new_goal}."
    except Exception as e:
        return str(e)
