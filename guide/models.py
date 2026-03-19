from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    academic_year = models.CharField(max_length=20, blank=True, default="")
    department = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(max_length=120, blank=True, default="")
    icon = models.ImageField(
        upload_to="profile_icons/",
        blank=True,
        null=True,
    )
    # compress pictures
    def save(self, *args, **kwargs):
        if self.icon and hasattr(self.icon.file, "content_type"):
            img = Image.open(self.icon)
            img = img.convert("RGB")
            img.thumbnail((300, 300))
            output = BytesIO()
            img.save(output, format="JPEG", quality=75)
            output.seek(0)
            self.icon = InMemoryUploadedFile(
                output, "ImageField", self.icon.name.split(".")[0] + ".jpg",
                "image/jpeg", sys.getsizeof(output), None
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    main = models.CharField(max_length=64)
    sub = models.CharField(max_length=64, blank=True, default="")
    description = models.CharField(max_length=120, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=300)
    address = models.CharField(max_length=256, blank=True, default="")
    rating = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    image_description = models.CharField(max_length=255, blank=True, null=True, help_text="Image description")
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

    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True,
    )
    # compress pictures
    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image.file, "content_type"):
            img = Image.open(self.image)
            img = img.convert("RGB")
            img.thumbnail((1200, 1200))
            output = BytesIO()
            img.save(output, format="JPEG", quality=75)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output, "ImageField", self.image.name.split(".")[0] + ".jpg",
                "image/jpeg", sys.getsizeof(output), None
            )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
    


class Comment(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to="comment_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image.file, "content_type"):
            img = Image.open(self.image)
            img = img.convert("RGB")
            img.thumbnail((800, 800))
            output = BytesIO()
            img.save(output, format="JPEG", quality=75)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output, "ImageField", self.image.name.split(".")[0] + ".jpg",
                "image/jpeg", sys.getsizeof(output), None
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Comment on {self.post.title} by {self.author}"


class CollectionList(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="collections",
    )
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(
        Post,
        related_name="in_collections",
        blank=True,
    )

    class Meta:
        unique_together = [["owner", "name"]]

    def __str__(self) -> str:
        return f"{self.owner.username} – {self.name}"


class News(models.Model):
    title = models.TextField()
    content = models.TextField(blank=True, default="")
    link = models.URLField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return self.title[:50] if len(self.title) > 50 else self.title

