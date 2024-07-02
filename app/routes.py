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

@main.route('/set_budget', methods=['POST'])
def set_budget():
    amount=request.json.get('amount')
    chatbot.budget=amount
    return jsonify({"response": f"Budget set to {amount}."})

@main.route('/advice', methods=['GET'])
def advice():
    response=chatbot.provide_advice()
    return jsonify({"response": response})