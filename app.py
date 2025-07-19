from flask import app, render_template
from bot import check_price, login


@app.route("/")
def show_signals():
    try:
        api = login()
    except Exception as e:
        print("❌ Login failed:", e)
        return "Login failed: " + str(e)

    signals = []

    for stock in stock:
        try:
            ltp = check_price(api, stock["symbol"], stock["token"])
            print(f"{stock['symbol']} → LTP: {ltp}")
            if ltp:
                action = "Buy" if ltp < 1000 else "Sell"  # dummy logic
                signals.append({
                    "symbol": stock["symbol"],
                    "price": ltp,
                    "action": action,
                    "target_buy": round(ltp * 0.98, 2),
                    "target_sell": round(ltp * 1.02, 2),
                    "stop_loss": round(ltp * 0.95, 2)
                })
        except Exception as e:
            print(f"⚠️ Error fetching {stock['symbol']}: {e}")

    # ✅ Fix: Always send a list, even if empty
    return render_template("index.html", signals=signals or [])
