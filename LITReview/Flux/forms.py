from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from Flux.models import Ticket, Review

RATING_CHOICE = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre'
        }


class ReviewForm(forms.Form):
    headline = forms.CharField(max_length=128, label="Titre")
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICE, label="Note")
    body = forms.CharField(max_length=8192, label="Commentaires", widget=forms.Textarea)
