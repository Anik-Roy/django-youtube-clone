from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CreateNewUser(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password1 = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'}))
    password2 = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-type your password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(
        required=True,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class EditProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = UserProfile
        exclude = ('user', )


