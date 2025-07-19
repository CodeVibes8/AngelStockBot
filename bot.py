# bot.py
from SmartApi import SmartConnect

# SmartAPI login
def login():
    obj = SmartConnect(api_key="your_api_key")
    data = obj.generateSession("clientcode", "password", "totp_here")
    return obj

# Check price function
# bot.py

def check_price(obj, symbol, token):
    try:
        data = {
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "symboltoken": token
        }
        ltp_data = obj.ltpData(data)
        print("🔎 Raw LTP response:", ltp_data)

        # Check structure and status
        if ltp_data.get("status") and ltp_data.get("data") and "ltp" in ltp_data["data"]:
            return ltp_data["data"]["ltp"]
        else:
            print(f"⚠️ No LTP for {symbol}: {ltp_data}")
            return None
    except Exception as e:
        print(f"❌ Exception in check_price for {symbol}: {e}")
        return None
