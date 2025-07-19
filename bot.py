# bot.py
from SmartApi import SmartConnect

# SmartAPI login
def login():
    obj = SmartConnect(api_key="your_api_key")
    data = obj.generateSession("clientcode", "password", "totp_here")
    return obj

# Check price function
def check_price(obj, symbol, token):
    data = {
        "exchange": "NSE",
        "tradingsymbol": symbol,
        "symboltoken": token
    }
    ltp_data = obj.ltpData(data)
    if ltp_data['status']:
        ltp = ltp_data['data']['ltp']
        return ltp
    return None
