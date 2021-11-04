from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from LITReview import settings


class Ticket(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])
    body = models.CharField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

