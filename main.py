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

    requests.post(url, json=payload)


@app.route("/")
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    print("DATA RECEIVED:", data)

    signal = data.get("signal", "Unknown").upper()
    ticker = data.get("ticker", "N/A")
    tf = data.get("timeframe", "N/A")
    price = data.get("price", "N/A")

    if signal == "CANDLE_KUNING":
        msg = f"""🟡 <b>CANDLE KUNING</b>

Ticker: {ticker}
TF: {tf}
Price: {price}

Breakout detected"""

    elif signal == "SHARK_IN":
        msg = f"""🦈 <b>SHARK IN</b>

Ticker: {ticker}
TF: {tf}
Price: {price}

Early institutional activity"""

    elif signal == "EARLY SHARK DETECTED":
        msg = f"""🔵 <b>EARLY ALERT</b>

Ticker: {ticker}
Price: {price}
TF: {tf}

Status: PRE-ENTRY SIGNAL
Risk: MEDIUM
Action: WAIT CONFIRMATION"""

    else:
        msg = f"""⚠️ Unknown signal

Ticker: {ticker}

Raw:
{data}"""

    send_message(msg)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)