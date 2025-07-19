import json
from .smartapi_connect import login

def load_stocks():
    return json.load(open("bot/stocks.json"))

def get_signals():
    obj = login()
    signals = []
    for s in load_stocks():
        d = obj.ltpData("NSE", s["symbol"], s["token"])
        if not d["status"]:
            continue
        price = d["data"]["ltp"]
        action = ("BUY" if price <= s["target_buy"]
                  else "SELL" if price >= s["target_sell"]
                  else "HOLD")
        signals.append({
            "symbol": s["symbol"],
            "price": price,
            "action": action,
            "target_buy": s["target_buy"],
            "target_sell": s["target_sell"],
            "stop_loss": s["stop_loss"]
        })
    return signals
