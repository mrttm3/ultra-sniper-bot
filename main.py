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
Raw: {data}"""

    send_message(msg)

    return {"status": "ok"}