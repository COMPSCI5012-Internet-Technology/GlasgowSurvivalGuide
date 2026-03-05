from django.contrib import admin
from guide.models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "main", "sub")
    search_fields = ("name", "main", "sub")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "address")