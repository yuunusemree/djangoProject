from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'comment_input', 'placeholder': 'username'}),
            'email': EmailInput(attrs={'class': 'comment_input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'comment_input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'comment_input', 'placeholder': 'last_name'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Erzurum', 'Erzurum')
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'comment_input', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'comment_input', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'comment_input', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'comment_input', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'fileinput', 'placeholder': 'image'})
        }