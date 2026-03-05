from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# post category, can have main category(life or school)and sub category(resturant or different colleges)
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    main = models.CharField(max_length=64)
    sub = models.CharField(max_length=64, blank=True, default="")
    description = models.CharField(max_length=120, blank=True, default="")

    def __str__(self) -> str:
        return self.name

# post details. 
class Post(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=300)
    address = models.CharField(max_length=256, blank=True, default="")
    rating = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    audio = models.URLField(blank=True, default="")
    video = models.URLField(blank=True, default="")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    liked_by = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True,
    )
    saved_by = models.ManyToManyField(
        User,
        related_name="saved_posts",
        blank=True,
    )

    def __str__(self) -> str:
        return self.title
