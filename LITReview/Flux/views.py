from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from Flux import forms
from Flux.models import Ticket


@login_required
def homepage_view(request):
    return render(request, 'flux/homepage.html')


@login_required
def my_flux_view(request):
    my_ticket = Ticket.objects.filter(user=request.user)
    return render(request, 'flux/my_flux.html', context={'tickets': my_ticket})


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

    return render(request, 'flux/create_ticket.html', context={'form': form})


@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_ticket.is_valid():
            edit_ticket.save()
            return redirect('my-flux')

    return render(request, 'flux/modify_ticket.html', context={'form': edit_ticket})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.image.delete()
    ticket.delete()
    message = f"Le ticket '{ticket.title}' a bien été supprimé"

    return render(request, 'flux/my_flux.html', context={'message': message})
