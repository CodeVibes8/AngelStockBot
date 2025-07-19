from SmartApi import SmartConnect
import os
import pyotp
import json

def load_config():
    with open("config.json") as f:
        config = json.load(f)
    os.environ["API_KEY"] = config["api_key"]
    os.environ["CLIENT_ID"] = config["client_id"]
    os.environ["MPIN"] = config["mpin"]
    os.environ["TOTP_SECRET"] = config["totp_secret"]

load_config()  # Call this before using login()


def login():
    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    data = obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    )
    return obj
