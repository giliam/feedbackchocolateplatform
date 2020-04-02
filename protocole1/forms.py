from django import forms
from django.utils.translation import gettext as _


class ConnectionForm(forms.Form):
    username = forms.CharField(label=_("User name"), max_length=150)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
