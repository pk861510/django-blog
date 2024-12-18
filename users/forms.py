from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    about = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email','about','password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    number = forms.NumberInput()

    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image','about']
