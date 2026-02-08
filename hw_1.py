"""from flask import Flask

app = Flask(__name__)
@app.route(")
def home():
    return 'Hello, World!'

if __name__ =="__main__":
    app.run(debug=True)"""

# Тут 2 проблемы. Стоит одна незакрытая кавычка, а также не указанный путь. Все находится в @app.route


"2"
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return 'Hello, Flask!'

@app.route("/user/<raw_data>")
def create_user(raw_data):
    data = {
        "data": raw_data
    }


@app.route("/user/<name>")
def user(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run(debug=True)