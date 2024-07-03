from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    budget = db.Column(db.Float, default=0.0)
    savings_goal = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    credit_balance = db.Column(db.Float, default=0.0)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'bank' or 'credit'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
