import datetime
import requests
import xml.etree.ElementTree as ET
from dateutil import tz

FF_XML = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
TIMEZONE = "Europe/Moscow"


def fetch_today_events():
    r = requests.get(FF_XML, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.content)

    # Today in FF format (feed uses e.g. 08-25-2025)
    today = datetime.datetime.now(tz.gettz(TIMEZONE)).strftime("%m-%d-%Y")

    events = []
    for ev in root.findall(".//event"):
        date = (ev.findtext("date") or "").strip()
        if date != today:
            continue
        impact = (ev.findtext("impact") or "").strip()

        title = (ev.findtext("title") or "").strip()
        cur = (ev.findtext("country") or "").strip()
        time_ = (ev.findtext("time") or "").strip()
        forecast = (ev.findtext("forecast") or "").strip()
        prev = (ev.findtext("previous") or "").strip()
        url = (ev.findtext("url") or "").strip()

        events.append({
            "date": date, "time": time_, "impact": impact, "title": title,
            "cur": cur, "forecast": forecast, "previous": prev, "url": url
        })
    return events
