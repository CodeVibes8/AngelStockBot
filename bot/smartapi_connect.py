import os
from SmartApi import SmartConnect
import pyotp

def login():
    obj = SmartConnect(api_key=os.getenv("CLIENT_ID"))
    totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()

    data = obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    )
    print("CLIENT_ID:", os.getenv("CLIENT_ID"))
    print("MPIN:", os.getenv("MPIN"))
    print("TOTP:", pyotp.TOTP(os.getenv("TOTP_SECRET")).now())
    print("API_KEY:", os.getenv("API_KEY"))

    return obj
