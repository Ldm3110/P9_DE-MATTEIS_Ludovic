from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField, Q, Count
from django.shortcuts import render, redirect, get_object_or_404

from Abonnements.models import UserFollows
from Connexion.models import User
from Flux import forms
from Flux.models import Ticket, Review

"""
BASIC VIEWS
"""


@login_required
def homepage_view(request):
    user_tickets = get_users_viewable_tickets(request, request.user)
    user_tickets = user_tickets.annotate(content_type=Value('TICKET', CharField()))
    user_tickets = user_tickets.annotate(num_reviews=Count('review'))

    user_reviews = get_users_viewable_reviews(request, request.user)
    user_reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = sorted(
        chain(user_tickets, user_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {'tickets': tickets,
               'user_reviews': user_reviews}

    return render(request, 'flux/homepage.html', context)


@login_required
def my_flux_view(request):
    my_ticket = Ticket.objects.filter(user=request.user)
    my_ticket = my_ticket.annotate(content_type=Value('TICKET', CharField()))
    my_review = Review.objects.filter(user=request.user)
    my_review = my_review.annotate(content_type=Value('REVIEW', CharField()))

    my_flux = sorted(chain(my_ticket, my_review),
                     key=lambda post: post.time_created,
                     reverse=True
                     )

    return render(request, 'my_flux/my_flux.html', context={'my_flux': my_flux})


"""
TICKET
"""


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('homepage')

    return render(request, 'creation/create_ticket.html', context={'form': form})


@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    image = ticket.image
    edit_ticket = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_ticket.is_valid():
            if not ticket.image:
                image.delete()
            edit_ticket.save()
            return redirect('my-flux')

    return render(request, 'creation/modify_ticket.html', context={'form': edit_ticket})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.image.delete()
        ticket.delete()
        return redirect('my-flux')

    return render(request, 'my_flux/my_flux.html')


"""
REVIEW
"""


@login_required
def create_review(request, ticket_id):
    affected_ticket = get_object_or_404(Ticket, id=ticket_id)
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            rating = form.cleaned_data['rating']
            body = form.cleaned_data['body']

            Review.objects.create(
                user_id=request.user.id,
                ticket_id=ticket_id,
                headline=headline,
                rating=rating,
                body=body
            )
            return redirect('homepage')

    return render(request, 'creation/create_review.html', context={'form': form, 'ticket': affected_ticket})


@login_required
def modify_review(request, review_id):
    this_review = get_object_or_404(Review, id=review_id)
    affected_ticket = get_object_or_404(Ticket, id=this_review.ticket_id)
    review_form = forms.ReviewForm(instance=this_review)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST, instance=this_review)
        if review_form.is_valid():
            review_form.save()
            return redirect('my-flux')

    context = {
        'rev': this_review,
        'ticket': affected_ticket,
        'form': review_form
    }

    return render(request, 'creation/modify_review.html', context)


@login_required
def delete_review(request, review_id):
    review_to_delete = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review_to_delete.delete()
        return redirect('my-flux')

    return render(request, 'my_flux/my_flux.html')


"""
TICKET AND REVIEW IN THE SAME TIME
"""


def ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    context = {
        'ticket': ticket_form,
        'review': review_form
    }
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            headline = review_form.cleaned_data['headline']
            rating = review_form.cleaned_data['rating']
            body = review_form.cleaned_data['body']

            Review.objects.create(
                user_id=request.user.id,
                ticket_id=ticket.id,
                headline=headline,
                rating=rating,
                body=body
            )
            return redirect('homepage')

    return render(request, 'creation/ticket-review.html', context)


"""
UTILITIES
"""


def get_users_viewable_reviews(request, user):
    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(
        Q(user=user) |
        Q(ticket__in=[ticket.id for ticket in tickets])
    )
    print(reviews)

    return reviews


def get_users_viewable_tickets(request, user):
    followed_by = UserFollows.objects.filter(user=user)
    tickets = Ticket.objects.filter(
        Q(user=user) |
        Q(user__in=[user.followed_user for user in followed_by])
    )

    return tickets
