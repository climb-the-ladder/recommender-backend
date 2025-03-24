from flask import Flask
from routes.recommendations import recommendation

app = Flask(__name__)
app.register_blueprint(recommendation)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
