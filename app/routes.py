from flask import Blueprint, render_template
from flask import request, jsonify
from .chatbot import BudgetChatbot

main=Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

chatbot=BudgetChatbot()

@main.route('/chat', methods=['POST'])
def chat():
    message=request.json.get('message')
    response=chatbot.respond(message)
    return jsonify({"response": response})