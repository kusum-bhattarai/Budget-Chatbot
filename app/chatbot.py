import nltk
from nltk.tokenize import word_tokenize

class BudgetChatbot:
    def __init__(self):
        self.intents={
            "greeting": ["hello", "hi", "hey"],
            "goodbye": ["bye", "goodbye"],
            "thanks": ["thanks", "thank you"],
        }

    def respond(self, message):
        tokens = word_tokenize(message.lower())
        for intent, keywords in self.intents.items():
            if any(token in keywords for token in tokens):
                return self.get_response(intent)
        return "I am not sure how to respond to that."
    
    def get_response(self, intent):
        responses={
            "greeting": "Hello! How can I assist you with your budget today?",
            "goodbye": "Goodbye! Have a great day!",
            "thanks": "You're welcome!"
        }
        return responses.get(intent, "I didn't understand that.")