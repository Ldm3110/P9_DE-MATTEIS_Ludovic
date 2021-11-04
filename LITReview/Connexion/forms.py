from django import forms
from django.core.exceptions import ValidationError

from Connexion.models import User


class UserForm(forms.Form):
    username = forms.CharField(max_length=50, label="Nom d'utilisateur")
    password = forms.CharField(max_length=256, label="Mot de passe", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Indiquez votre pseudo ')
    password1 = forms.CharField(max_length=256, label='Indiquez votre mot de passe ', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=256, label='Confirmez votre mot de passe ', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "Les mots de passes ne sont pas identiques !"
            )
        return password2

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password2']
        )
        if commit:
            user.save()
        return user
