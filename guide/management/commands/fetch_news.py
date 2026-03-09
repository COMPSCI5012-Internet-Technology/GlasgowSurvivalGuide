from django.core.management.base import BaseCommand
from django.utils import timezone

from guide.models import News
from guide.services.news_service import get_news_for_daily_fetch


class Command(BaseCommand):
    help = "Fetch news (Mock or Real per settings.USE_MOCK_API) and replace News table with up to 5 items."

    def handle(self, *args, **options):
        items = get_news_for_daily_fetch(limit=5)
        News.objects.all().delete()
        created = 0
        for item in items:
            if not item.get("link"):
                continue
            News.objects.create(
                title=item.get("title") or "",
                content=item.get("content") or "",
                link=item["link"],
                time=item.get("time") or timezone.now(),
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Fetched and saved {created} news item(s)."))
