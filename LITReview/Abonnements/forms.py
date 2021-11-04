from django import forms


class UserFollowsForm(forms.Form):
    user = forms.CharField(max_length=60, label="Nom d'utilisateur", required=True)
