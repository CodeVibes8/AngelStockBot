# app.py
from flask import Flask, render_template
import threading, time
import os, json, pyotp
from bot.logic import get_signals
from SmartApi import SmartConnect

app = Flask(__name__)

# Global variables
cached_signals = []
smart_api = None


def load_config():
    with open("config.json") as f:
        config = json.load(f)
        os.environ["API_KEY"] = config["api_key"]
        os.environ["CLIENT_ID"] = config["client_id"]
        os.environ["MPIN"] = config["mpin"]
        os.environ["TOTP_SECRET"] = config["totp_secret"]


def login():
    global smart_api
    smart_api = SmartConnect(api_key=os.getenv("API_KEY"))
    data = smart_api.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    )
    print("✅ Logged in successfully.")


def refresh_signals():
    global cached_signals
    while True:
        try:
            print("🔄 Fetching signals...")
            cached_signals = get_signals(smart_api)
            print(f"✅ {len(cached_signals)} signals updated.")
        except Exception as e:
            print(f"❌ Error updating signals: {e}")
        time.sleep(30)  # update every 30 seconds


@app.before_first_request
def init_bot():
    load_config()
    login()
    threading.Thread(target=refresh_signals, daemon=True).start()


@app.route("/")
def home():
    return render_template("index.html", signals=cached_signals)


if __name__ == "__main__":
    app.run(debug=True)
