import os, textwrap
from telegram import Bot
from telegram.constants import ParseMode

from news.fetch_today_events import fetch_today_events
from news.build_message import build_message

# --- CONFIG ---
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_today_digest():
    events = fetch_today_events()
    msgs = build_message(events)
    bot = Bot(BOT_TOKEN)
    if isinstance(msgs, list):
        for m in msgs:
            bot.send_message(CHAT_ID, m, parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_message(CHAT_ID, msgs, parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    send_today_digest()
