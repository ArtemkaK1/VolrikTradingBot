import asyncio
from telegram import Bot
from telegram.constants import ParseMode

from news.fetch_today_events import fetch_today_events
from news.build_message import build_message
from env_manager.env_manager import BOT_TOKEN, CHAT_ID
from trading.bingx_client import BingXClient


def send_today_digest():
    events = fetch_today_events()
    msgs = build_message(events)
    bot = Bot(BOT_TOKEN)
    if isinstance(msgs, list):
        for m in msgs:
            asyncio.run(bot.send_message(CHAT_ID, m, parse_mode=ParseMode.MARKDOWN))
    else:
        asyncio.run(bot.send_message(CHAT_ID, msgs, parse_mode=ParseMode.MARKDOWN))


if __name__ == "__main__":
    client = BingXClient(is_demo=False)
    print(client.get_account_balance())
