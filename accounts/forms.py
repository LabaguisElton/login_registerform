from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            matching_usernames = list(
                User.objects.filter(email__iexact=username).values_list('username', flat=True)[:2]
            )
            if len(matching_usernames) > 1:
                raise ValidationError(
                    'Multiple accounts use this email. Please log in with your username.'
                )
            if matching_usernames:
                self.cleaned_data['username'] = matching_usernames[0]

        return super().clean()