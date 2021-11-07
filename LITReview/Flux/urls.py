from django.urls import path

from Flux import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('my_flux/', views.my_flux_view, name='my-flux'),
    path('create_ticket/', views.create_ticket, name='create-ticket'),
    path('modify_ticket/<int:ticket_id>', views.modify_ticket, name='modify-ticket'),
    path('delete_ticket/<int:ticket_id>', views.delete_ticket, name='delete-ticket'),
    path('create_review/<int:ticket_id>', views.create_review, name='create-review'),
    path('modify_review/<int:review_id>', views.modify_review, name='modify-review'),
    path('delete_review/<int:review_id>', views.delete_review, name='delete-review'),
]
