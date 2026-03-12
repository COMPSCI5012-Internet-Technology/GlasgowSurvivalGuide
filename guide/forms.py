from django import forms
from django.contrib.auth import authenticate, get_user_model

from guide.models import CollectionList, Comment, Post

User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='UofG Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'email@gla.ac.uk',
        }),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError('Email is required.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        username = email[:150]
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label='UofG Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'email@gla.ac.uk',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').strip().lower()
        password = cleaned_data.get('password')
        if not email or not password:
            return cleaned_data
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid email or password.')
        user = authenticate(
            username=user.username,
            password=password,
        )
        if user is None:
            raise forms.ValidationError('Invalid email or password.')
        cleaned_data['user'] = user
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "description",
            "address",
            "rating",
            "category",
            "tags",
            "image",
            "status",
            'image_description',
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter post title"}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Write a description for your post...",
                    "rows": 5,
                }
            ),
            "address": forms.TextInput(attrs={"placeholder": "Search location..."}),
            "rating": forms.NumberInput(attrs={"min": 0, "max": 5}),
        }
        labels = {
            "address": "Location",
            "status": "Public (visible to everyone)",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", "image")
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Write a comment...", "rows": 3}),
        }


class CollectionCreateForm(forms.Form):
    name = forms.CharField(
        max_length=20,
        label="Collection name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Favorites"}),
    )
    status = forms.BooleanField(
        required=False,
        initial=True,
        label="Open (visible to others)",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("Name is required.")
        if self.user and CollectionList.objects.filter(owner=self.user, name=name).exists():
            raise forms.ValidationError("You already have a collection with this name.")
        return name
