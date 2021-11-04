from django.urls import path

from Abonnements import views

urlpatterns = [
    path('', views.subscription_view, name='subscribe'),
]
