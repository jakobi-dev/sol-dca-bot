import os
import json
import urllib.request
import urllib.parse

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
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
    data    = fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=solana")
    coin    = data[0]
    current = coin["current_price"]
    high    = coin["high_24h"]
    low     = coin["low_24h"]

    position = (current - low) / ((high - low) or 1)
    pct = round(position * 100)

    if position <= 0.25:
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
        print(f"No alert — signal is {signal}.")

if __name__ == "__main__":
    main()
