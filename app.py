from flask import Flask
from flask_cors import CORS
from routes.recommendations import recommendation
from routes.chatbot import chatbot

app = Flask(__name__)
CORS(app) 

app.register_blueprint(recommendation)
app.register_blueprint(chatbot)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
