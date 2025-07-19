import os
from SmartApi import SmartConnect
import pyotp

def login():
    obj = SmartConnect(api_key=os.getenv("CLIENT_ID"))
    totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()

    data = obj.generateSession(
        clientCode=os.getenv("CLIENT_ID"),
        password=os.getenv("MPIN"),
        totp=totp
    )
    return obj
