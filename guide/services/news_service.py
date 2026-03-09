import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

from django.conf import settings

logger = logging.getLogger(__name__)


def get_news_for_daily_fetch(limit=5):
    if getattr(settings, "USE_MOCK_API", True):
        return _fetch_from_mock(limit)
    return _fetch_from_real(limit)


def _fetch_from_mock(limit):
    mock_path = Path(settings.BASE_DIR) / "mock_data" / "news.json"
    if not mock_path.exists():
        return []
    with open(mock_path, encoding="utf-8") as f:
        data = json.load(f)
    results = data.get("results") or []
    out = []
    for item in results[:limit]:
        pub = item.get("pubDate") or ""
        try:
            if pub.endswith("Z"):
                pub = pub.replace("Z", "+00:00")
            time_val = datetime.fromisoformat(pub)
        except (ValueError, TypeError):
            time_val = datetime.now()
        out.append({
            "title": item.get("title") or "",
            "content": item.get("description") or "",
            "link": item.get("link") or "",
            "time": time_val,
        })
    return out


def _fetch_from_real(limit):
    api_key = getattr(settings, "NEWSDATA_API_KEY", "") or ""
    if not api_key:
        logger.warning("NEWSDATA_API_KEY is not set; cannot fetch from NewsData.io")
        return []
    url = (
        "https://newsdata.io/api/1/latest"
        f"?apikey={api_key}&q=Glasgow&country=gb&language=en&size={min(limit, 50)}"
    )
    try:
        req = Request(url, headers={"User-Agent": "GlasgowSurvivalGuide/1.0"})
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except (URLError, OSError, ValueError, KeyError) as e:
        logger.exception("NewsData.io request failed: %s", e)
        return []
    if data.get("error") or data.get("status") == "error":
        logger.warning(
            "NewsData.io API error: %s",
            data.get("message") or data.get("error") or "unknown",
        )
        return []
    results = data.get("results") or data.get("articles") or []
    out = []
    for item in results[:limit]:
        pub = item.get("pubDate") or ""
        try:
            if pub and str(pub).endswith("Z"):
                pub = str(pub).replace("Z", "+00:00")
            time_val = datetime.fromisoformat(pub) if pub else datetime.now()
        except (ValueError, TypeError):
            time_val = datetime.now()
        link = item.get("link") or item.get("url") or ""
        if not link:
            continue
        out.append({
            "title": item.get("title") or "",
            "content": item.get("description") or "",
            "link": link,
            "time": time_val,
        })
    return out
