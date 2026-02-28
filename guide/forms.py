from django import forms
from django.contrib.auth import authenticate, get_user_model

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
