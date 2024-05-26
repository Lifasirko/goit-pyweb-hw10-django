from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ModelForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

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


class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain_override
                domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )


class CustomSetPasswordForm(SetPasswordForm):
    pass
