import json
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

def load_stocks():
    with open("bot/stocks.json") as f:
        return json.load(f)

def get_historical_candles(obj, symbol, token, interval="5minute", days=5):
    try:
        data = obj.getCandleData(
            exchange="NSE",
            symboltoken=token,
            interval=interval,
            fromdate="2025-07-15 09:15",
            todate="2025-07-19 15:30"
        )

        candles = data.get("data", [])
        if not candles:
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

def get_signals(obj):
    signals = []

    for stock in load_stocks():
        symbol = stock["symbol"]
        token = stock["token"]

        # Fetch historical candles
        df = get_historical_candles(obj, symbol, token)
        if df is None or len(df) < 50:
            continue

        try:
            # Technical Indicators
            ema_20 = EMAIndicator(close=df["close"], window=20).ema_indicator()
            ema_50 = EMAIndicator(close=df["close"], window=50).ema_indicator()
            rsi = RSIIndicator(close=df["close"], window=14).rsi()
            atr = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range()

            df["ema_20"] = ema_20
            df["ema_50"] = ema_50
            df["rsi"] = rsi
            df["atr"] = atr

            latest = df.iloc[-1]

            # Live price
            price = obj.ltpData(exchange="NSE", tradingsymbol=symbol, symboltoken=token)["data"]["ltp"]

            action = "HOLD"
            target = None
            stop_loss = None

            # Buy condition
            if latest["ema_20"] > latest["ema_50"] and latest["rsi"] > 55:
                action = "BUY"
                target = round(price + 2 * latest["atr"], 2)
                stop_loss = round(price - latest["atr"], 2)

            # Sell condition
            elif latest["ema_20"] < latest["ema_50"] and latest["rsi"] < 45:
                action = "SELL"
                target = round(price - 2 * latest["atr"], 2)
                stop_loss = round(price + latest["atr"], 2)

            if action != "HOLD":
                signals.append({
                    "symbol": symbol,
                    "price": round(price, 2),
                    "action": action,
                    "target": target,
                    "stop_loss": stop_loss,
                    "rsi": round(latest["rsi"], 2),
                    "atr": round(latest["atr"], 2)
                })

        except Exception as e:
            print(f"❌ Signal generation failed for {symbol}: {e}")

    return signals
