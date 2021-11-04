from django.urls import path

from Abonnements import views

urlpatterns = [
    path('', views.subscription_view, name='subscribe'),
    path('delete_subscription/<int:subscription_id>', views.delete_subscription, name='delete-subscription'),
]
