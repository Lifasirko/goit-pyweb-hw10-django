from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Author, Quote


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date', 'born_location', 'bio']


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'tags']
