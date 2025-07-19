# bot/logic.py
import json
from .smartapi_connect import login

def load_stocks():
    with open("bot/stocks.json") as f:
        return json.load(f)

def get_signals():
    obj = login()
    signals = []

    for s in load_stocks():
        try:
            data = {
                "exchange": "NSE",
                "tradingsymbol": s["symbol"],
                "symboltoken": s["token"]
            }
            d = obj.ltpData(data)

            if not d.get("status"):
                print(f"⚠️ Invalid response for {s['symbol']}: {d}")
                continue

            price = d["data"]["ltp"]
            action = (
                "BUY" if price <= s["target_buy"]
                else "SELL" if price >= s["target_sell"]
                else "HOLD"
            )

            signals.append({
                "symbol": s["symbol"],
                "price": price,
                "action": action,
                "target_buy": s["target_buy"],
                "target_sell": s["target_sell"],
                "stop_loss": s["stop_loss"]
            })
        except Exception as e:
            print(f"❌ Error for {s['symbol']}: {e}")
    return signals
