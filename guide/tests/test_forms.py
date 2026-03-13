
from django.contrib.auth import get_user_model
from django.test import TestCase

from guide.forms import PostForm, RegisterForm
from guide.models import Category, Post, UserProfile

User = get_user_model()

class RegisterFormTests(TestCase):
    def test_valid_student_email_and_matching_passwords_is_valid(self):
        form = RegisterForm(data={
            "email": "test@student.gla.ac.uk",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_email_must_end_with_student_gla_ac_uk(self):
        form = RegisterForm(data={
            "email": "user@gmail.com",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn(
            "Only @student.gla.ac.uk email addresses are allowed for registration.",
            form.errors["email"],
        )

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            username="existing",
            email="existing@student.gla.ac.uk",
            password="existingpass",
        )
        form = RegisterForm(data={
            "email": "existing@student.gla.ac.uk",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("A user with this email already exists.", form.errors["email"])

    def test_password_mismatch_rejected(self):
        form = RegisterForm(data={
            "email": "newuser@student.gla.ac.uk",
            "password1": "securepass123",
            "password2": "differentpass",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertIn("Passwords don't match.", form.errors["password2"])

    def test_save_creates_user_and_profile(self):
        form = RegisterForm(data={
            "email": "newuser@student.gla.ac.uk",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.email, "newuser@student.gla.ac.uk")
        self.assertEqual(user.username, "newuser@student.gla.ac.uk")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.email, "newuser@student.gla.ac.uk")


class PostFormTests(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            username="author",
            email="author@student.gla.ac.uk",
            password="testpass123",
        )
        self.category = Category.objects.create(
            name="life - food",
            main="life",
            sub="food",
        )

    def test_valid_minimal_data_is_valid(self):
        form = PostForm(data={
            "title": "Test Post",
            "description": "A short description",
            "rating": 3,
            "category": self.category.pk,
            "status": True,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_missing_required_fields_is_invalid(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("description", form.errors)

    def test_optional_address_audio_video_can_be_blank(self):
        form = PostForm(data={
            "title": "Test Post",
            "description": "A short description",
            "rating": 5,
            "category": self.category.pk,
            "address": "",
            "audio": "",
            "video": "",
            "status": True,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_rating_out_of_range_still_relies_on_model_validation(self):
        form = PostForm(data={
            "title": "Test Post",
            "description": "A short description",
            "rating": -1,
            "category": self.category.pk,
            "status": True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_save_creates_post_instance_without_author(self):
        form = PostForm(data={
            "title": "Test Post",
            "description": "A short description",
            "rating": 4,
            "category": self.category.pk,
            "address": "Glasgow",
            "audio": "https://example.com/audio.mp3",
            "video": "https://example.com/video.mp4",
            "status": True,
        })
        self.assertTrue(form.is_valid(), form.errors)
        post = form.save(commit=False)
        self.assertIsInstance(post, Post)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.category, self.category)
