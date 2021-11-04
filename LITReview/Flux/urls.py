from django.urls import path

from Flux import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('my_flux/', views.my_flux_view, name='my-flux'),
    path('create_ticket/', views.create_ticket, name='create-ticket')
]
