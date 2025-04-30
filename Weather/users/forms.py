from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'name@example.com',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Password'
        }),
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com'
        }),
        label='Email',
        max_length=30,

    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'readonly': True
    }))
    tg_username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'tg_username',
            'placeholder': 'Telegram Username'
    }))
    users_city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'city',
            'placeholder': 'New York'
    }))
    del_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'id': 'del_time',
            'placeholder': 'HH:MM'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'tg_username', 'users_city', 'del_time']