from . import db

class User(db.Model):
    id=db.column(db.Integer, primary_key=True)
    budget=db.Column(db.Float, default=0)
    expenses=db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Float, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)