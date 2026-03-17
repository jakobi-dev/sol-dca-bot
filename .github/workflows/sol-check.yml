import os
import json
import urllib.request
import urllib.parse

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }).encode()
    urllib.request.urlopen(url, data=data, timeout=10)

def main():
    ticker = fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=SOLUSDT")
    current = float(ticker["lastPrice"])
    high    = float(ticker["highPrice"])
    low     = float(ticker["lowPrice"])

    position = (current - low) / ((high - low) or 1)
    pct = round(position * 100)

    if position <= 0.33:
        signal = "BUY"
    elif position <= 0.66:
        signal = "DECENT"
    else:
        signal = "WAIT"

    print(f"SOL: ${current:.2f} | Low: ${low:.2f} | High: ${high:.2f} | {pct}% | Signal: {signal}")

    if signal == "BUY":
        msg = (
            f"🟢 <b>SOL DCA SIGNAL: BUY</b>\n\n"
            f"Now: <b>${current:.2f}</b>\n"
            f"24H Low: ${low:.2f} | High: ${high:.2f}\n"
            f"At {pct}% of today's range — near daily low.\n\n"
            f"Good time to DCA! 🎯"
        )
        send_telegram(msg)
        print("Telegram alert sent.")
    else:
        print("No alert — signal is not BUY.")

if __name__ == "__main__":
    main()
