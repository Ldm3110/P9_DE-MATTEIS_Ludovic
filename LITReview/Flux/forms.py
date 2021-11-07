from django import forms

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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'rating': 'Note',
            'body': 'Commentaires'
        }
        widgets = {
            'rating': forms.RadioSelect(choices=RATING_CHOICE),
            'body': forms.Textarea
        }
