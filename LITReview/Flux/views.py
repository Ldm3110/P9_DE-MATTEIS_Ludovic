from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Flux import forms


@login_required
def homepage_view(request):
    return render(request, 'flux/homepage.html')


@login_required
def my_flux_view(request):
    return render(request, 'flux/my_flux.html')


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

