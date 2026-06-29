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
    return "Ultra Sniper Bot Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    signal = data.get("signal", "").upper()
    ticker = data.get("ticker", "N/A")
    price = data.get("price", "N/A")
    tf = data.get("timeframe", "N/A")

    tf_map = {
        "1": "1m",
        "3": "3m",
        "5": "5m",
        "15": "15m",
        "30": "30m",
        "60": "1H",
        "240": "4H",
        "D": "1D",
        "W": "1W",
        "M": "1M"
    }
    tf = tf_map.get(str(tf), str(tf))

    if signal == "EARLY SHARK DETECTED":
        msg = f"""🟡 <b>EARLY INSTITUTIONAL SIGNAL</b>

📊 Pair : <b>{ticker}</b>
💰 Price : <b>{price}</b>
⏱ TF : <b>{tf}</b>

🧠 Status : PRE-ENTRY
⚠️ Risk : MEDIUM
🎯 Action : WAIT CONFIRMATION"""

    else:
        msg = f"""📊 {ticker}

Signal : {signal}
Price : {price}
TF : {tf}"""

    send_message(msg)
    return {"status": "ok"}, 200


    # Jika TradingView hantar JSON
    data = request.json or {}

    print(data)

    signal = data.get("signal", "").upper()
    ticker = data.get("ticker", "N/A")
    price = data.get("price", "N/A")
    tf = data.get("timeframe", "N/A")

    if signal == "EARLY SHARK DETECTED":

        msg = f"""
🟡 <b>EARLY INSTITUTIONAL SIGNAL</b>

━━━━━━━━━━━━━━

📊 Pair : <b>{ticker}</b>
💰 Price : <b>{price}</b>
⏱ TF : <b>{tf}</b>

━━━━━━━━━━━━━━

🧠 Status : PRE-ENTRY SIGNAL

⚠️ Risk : MEDIUM

📍 Action : WAIT CONFIRMATION
"""

    elif signal == "SHARK IN":

        msg = f"""
🦈 <b>SHARK IN</b>

📊 Pair : <b>{ticker}</b>

💰 Price : <b>{price}</b>

⏱ TF : <b>{tf}</b>

🔥 Institutional Buying Detected
"""

    elif signal == "BUY":

        msg = f"""
🟢 <b>BUY SIGNAL</b>

📊 Pair : <b>{ticker}</b>

💰 Entry : <b>{price}</b>

⏱ TF : <b>{tf}</b>

✅ Momentum Confirmed
"""

    elif signal == "SELL":

        msg = f"""
🔴 <b>SELL SIGNAL</b>

📊 Pair : <b>{ticker}</b>

💰 Entry : <b>{price}</b>

⏱ TF : <b>{tf}</b>

⚠️ Bearish Momentum
"""

    else:

        if "message" in data:
            msg = data["message"]
        else:
            msg = str(data)

    send_message(msg)

    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    