# app.py
from flask import Flask, render_template
from bot.logic import get_signals

app = Flask(__name__)

@app.route("/")
def show_signals():
    try:
        signals = get_signals()
        return render_template("index.html", signals=signals)
    except Exception as e:
        print("❌ Error getting signals:", e)
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
