import datetime
import html
from dateutil import tz

TIMEZONE = "Europe/Moscow"


def build_message(events):
    local_date = datetime.datetime.now(tz.gettz(TIMEZONE)).strftime("%a, %d %b %Y")
    hdr = f"*ForexFactory — {local_date}*"

    if not events:
        return hdr + "\nNo events for your filters today."

    lines = []
    for e in events:
        forecast = f" • Forecast: {e['forecast']}" if e['forecast'] else ""
        prev = f" • Prev: {e['previous']}" if e['previous'] else ""
        link = f" — [link]({e['url']})" if e['url'] else ""
        lines.append(
            f"• *{e['time']}* — *{e['cur']}* • {html.escape(e['title'])} "
            f"(_{e['impact']}_){forecast}{prev}{link}"
        )
    # Telegram msg limit ~4096 chars; chunk if needed
    chunks = []
    current = hdr
    for line in lines:
        candidate = current + "\n" + line
        if len(candidate) > 3800:
            chunks.append(current)
            current = hdr + "\n" + line
        else:
            current = candidate
    chunks.append(current)
    return chunks
