# bot/logic.py
import json

def load_stocks():
    with open("bot/stocks.json") as f:
        return json.load(f)

def get_signals(obj):  # <-- accepts SmartConnect session
    signals = []

    for s in load_stocks():
        try:
            d = obj.ltpData(
                exchange="NSE",
                tradingsymbol=s["symbol"],
                symboltoken=s["token"]
            )

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
