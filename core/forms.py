from django.contrib.auth import forms as auth_forms
from hacker import models as hacker_models


class SignupForm(auth_forms.UserCreationForm):

    class Meta:
        model = hacker_models.Hacker
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
