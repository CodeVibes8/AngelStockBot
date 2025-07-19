from flask import Flask, render_template
from bot.logic import get_signals

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", signals=get_signals())

if __name__ == "__main__":
    app.run(debug=True)
