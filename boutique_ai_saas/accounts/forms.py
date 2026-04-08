from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import UserProfile, UserRole

User = get_user_model()


class VendorSignupForm(forms.Form):
    business_name = forms.CharField(max_length=200)
    subdomain = forms.SlugField(max_length=50, help_text="Used as /<vendor>/ path and optional subdomain.")
    theme_color = forms.CharField(max_length=20, initial="#db2777")
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)


class ProfileLanguageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["language"]

