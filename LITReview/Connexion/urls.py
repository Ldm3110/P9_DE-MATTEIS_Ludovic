from django.urls import path

from Connexion import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.registration_view, name='registration'),
    path('logout/', views.logout_view, name='logout')
]