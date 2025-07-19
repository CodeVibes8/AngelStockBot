# bot/smartapi_connect.py
import os
from SmartApi import SmartConnect
import pyotp
import json

def load_config():
    with open("config.json") as f:
        config = json.load(f)
        os.environ["API_KEY"] = config["api_key"]
        os.environ["CLIENT_ID"] = config["client_id"]
        os.environ["MPIN"] = config["mpin"]
        os.environ["TOTP_SECRET"] = config["totp_secret"]

def login():
    load_config()

    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()

    obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=totp
    )

    return obj
