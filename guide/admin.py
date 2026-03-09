from django.contrib import admin, messages
from django.utils import timezone

from guide.models import Category, CollectionList, Comment, News, Post, Tag
from guide.services.news_service import get_news_for_daily_fetch


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "main", "sub")
    search_fields = ("name", "main", "sub")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "address")
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)


@admin.register(CollectionList)
class CollectionListAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    filter_horizontal = ("posts",)


def fetch_news_action(modeladmin, request, queryset):
    items = get_news_for_daily_fetch(limit=5)
    if not items:
        messages.warning(request, "No news items fetched; existing data kept.")
        return
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
    messages.success(request, f"Fetched and saved {created} news item(s).")


fetch_news_action.short_description = "Fetch news (Mock/Real per settings)"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "time")
    list_filter = ("time",)
    search_fields = ("title", "content",)
    actions = [fetch_news_action]
