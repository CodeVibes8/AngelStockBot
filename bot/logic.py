import os
import json
import time
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
from datetime import datetime, timedelta

def load_stocks():
    with open("bot/stocks.json") as f:
        return json.load(f)

def get_historical_candles(obj, symbol, token, exchange="NSE", interval="FIVE_MINUTE", days=5):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)

    try:
        params = {
            "exchange": exchange,
            "symboltoken": token,
            "interval": interval,
            "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
            "todate": to_date.strftime("%Y-%m-%d %H:%M")
        }

        data = obj.getCandleData(params)
        candles = data.get("data", [])

        if not candles or len(candles[0]) < 6:
            return None

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["close"] = pd.to_numeric(df["close"])
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])
        df["volume"] = pd.to_numeric(df["volume"])

        return df

    except Exception as e:
        print(f"❌ Error fetching candle data for {symbol}: {e}")
        return None

def get_signals(api):
    signals = []

    stock_path = os.path.join(os.path.dirname(__file__), "stocks.json")
    with open(stock_path) as f:
        stock_list = json.load(f)

    for stock in stock_list:
        symbol = stock.get("symbol")
        token = stock.get("token")
        exchange = stock.get("exchange", "NSE")

        if not symbol or not token:
            print(f"⚠️ Skipping invalid stock entry: {stock}")
            continue

        print(f"📊 Processing {symbol}...")

        df = get_historical_candles(api, symbol, token, exchange)
        if df is None or df.empty:
            print(f"❌ No historical data for {symbol}")
            continue

        try:
            df["ema"] = EMAIndicator(df["close"], window=20).ema_indicator()
            df["rsi"] = RSIIndicator(df["close"], window=14).rsi()
            df["atr"] = AverageTrueRange(df["high"], df["low"], df["close"], window=14).average_true_range()
            latest = df.iloc[-1]

            price = round(latest["close"], 2)
            rsi = round(latest["rsi"], 2)
            atr = round(latest["atr"], 2)
            ema = round(latest["ema"], 2)

            action = "HOLD"
            target = stop_loss = None

            if price > ema and rsi < 70:
                action = "BUY"
                target = round(price + atr, 2)
                stop_loss = round(price - atr, 2)
            elif price < ema and rsi > 30:
                action = "SELL"
                target = round(price - atr, 2)
                stop_loss = round(price + atr, 2)

            if action != "HOLD":
                signals.append({
                    "symbol": symbol,
                    "price": price,
                    "action": action,
                    "target": target,
                    "stop_loss": stop_loss,
                    "rsi": rsi,
                    "atr": atr
                })

        except Exception as e:
            print(f"❌ Signal processing failed for {symbol}: {e}")

    print(f"✅ Signals ready: {json.dumps(signals, indent=2)}")
    return signals
