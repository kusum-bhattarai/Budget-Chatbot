import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///budget_chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
