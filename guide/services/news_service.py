import json
from datetime import datetime
from pathlib import Path

from django.conf import settings


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
    return []
