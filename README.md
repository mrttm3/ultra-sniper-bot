from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    signal = data.get("signal", "Unknown")
    ticker = data.get("ticker", "N/A")
    tf = data.get("timeframe", "N/A")

    if signal == "CANDLE_KUNING":
        msg = f"""🟡 <b>CANDLE KUNING</b>

Ticker: {ticker}
TF: {tf}

Breakout detected"""

    elif signal == "SHARK_IN":
        msg = f"""🦈 <b>SHARK IN</b>

Ticker: {ticker}
TF: {tf}

Early institutional activity"""

    elif signal == "EARLY":
        msg = f"""🔵 <b>EARLY ALERT</b>

Ticker: {ticker}
TF: {tf}

Watchlist only"""

    else:
        msg = f"""⚠️ Unknown signal
Ticker: {ticker}"""

    send_message(msg)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)