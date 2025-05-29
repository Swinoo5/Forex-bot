
import requests
import asyncio
import numpy as np
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime

TELEGRAM_BOT_TOKEN = '7710846503:AAHIeibJ7eSIyF2_nEvA36Wfx2WL-pKmIPQ'
TELEGRAM_CHAT_ID = '1025923675'
BASE_COINS = ['BTC', 'ETH', 'BNB', 'LTC']
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_coin_pairs(base):
    url = f'https://www.macroaxis.com/invest/market/{base}-Crypto-Correlation'
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.find_all('tr')[1:]
        result = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                try:
                    coin = cols[0].text.strip()
                    corr = float(cols[2].text.strip())
                    if 0.9 <= corr <= 0.99:
                        result.append((base, coin, corr))
                except:
                    continue
        return result
    except Exception as e:
        return []

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    messages = []

    for base in BASE_COINS:
        pairs = get_coin_pairs(base)
        for base, coin, corr in pairs:
            messages.append(f"*{base}* and *{coin}* correlation: `{corr}`")

    if messages:
        message = "\n".join(messages)
    else:
        message = "No significant correlations found."

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(main())
