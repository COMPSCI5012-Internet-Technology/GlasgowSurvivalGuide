
from django.contrib.auth import get_user_model
from django.test import TestCase

from guide.forms import RegisterForm
from guide.models import UserProfile

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
