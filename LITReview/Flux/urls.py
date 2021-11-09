from django.urls import path

from Flux import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('create_ticket/', views.create_ticket, name='create-ticket'),
    path('create_review/<int:ticket_id>', views.create_review, name='create-review'),
    path('create_ticket_review/', views.ticket_and_review, name='ticket-review'),

    path('my_flux/', views.my_flux_view, name='my-flux'),
    path('my_flux/modify_ticket/<int:ticket_id>', views.modify_ticket, name='modify-ticket'),
    path('my_flux/delete_ticket/<int:ticket_id>', views.delete_ticket, name='delete-ticket'),
    path('my_flux/modify_review/<int:review_id>', views.modify_review, name='modify-review'),
    path('my_flux/delete_review/<int:review_id>', views.delete_review, name='delete-review'),

]
