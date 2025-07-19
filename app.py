from flask import Flask
from SmartApi import SmartConnect
import os, json, pyotp

app = Flask(__name__)  # <-- Important

def load_config():
    with open("config.json") as f:
        config = json.load(f)
        os.environ["API_KEY"] = config["api_key"]
        os.environ["CLIENT_ID"] = config["client_id"]
        os.environ["MPIN"] = config["mpin"]
        os.environ["TOTP_SECRET"] = config["totp_secret"]

load_config()

def login():
    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    data = obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    )
    return obj

@app.route("/")
def home():
    return "✅ Angel One Bot is running!"

if __name__ == "__main__":
    app.run()