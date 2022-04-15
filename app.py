from flask import Flask


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    # print(dir(mysql))
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
