from flask import Flask, render_template
from SmartApi import SmartConnect
import os, json, pyotp
from bot import check_price  # import from bot.py

app = Flask(__name__)

# Load secrets from config.json
def load_config():
    with open("config.json") as f:
        config = json.load(f)
        os.environ["API_KEY"] = config["api_key"]
        os.environ["CLIENT_ID"] = config["client_id"]
        os.environ["MPIN"] = config["mpin"]
        os.environ["TOTP_SECRET"] = config["totp_secret"]

load_config()

# Login to SmartAPI
def login():
    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    )
    return obj

# Example stock data (can load from JSON file too)
stocks = [
    {"symbol": "RELIANCE-EQ", "token": "2885"},
    {"symbol": "INFY-EQ", "token": "1594"},
    {"symbol": "TCS-EQ", "token": "11536"},
]

@app.route("/")
def show_signals():
    api = login()
    signals = []

    for stock in stocks:
        ltp = check_price(api, stock["symbol"], stock["token"])
        if ltp:
            action = "Buy" if ltp < 1000 else "Sell"  # dummy logic
            signals.append({
                "symbol": stock["symbol"],
                "price": ltp,
                "action": action,
                "target_buy": round(ltp * 0.98, 2),
                "target_sell": round(ltp * 1.02, 2),
                "stop_loss": round(ltp * 0.95, 2)
            })

    return render_template("index.html", signals=signals)

if __name__ == "__main__":
    app.run()
