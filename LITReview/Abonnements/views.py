from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from Abonnements.forms import UserFollowsForm
from Abonnements.models import UserFollows
from Connexion.models import User


@login_required
def subscription_view(request):
    form = UserFollowsForm()
    followers = UserFollows.objects.filter(user_id=request.user)
    followed_by = UserFollows.objects.filter(followed_user_id=request.user)
    message = ""
    if request.method == 'POST':
        pseudo = request.POST['user']
        try:
            user = User.objects.get(username=pseudo)
            UserFollows.objects.create(
                user=request.user,
                followed_user=user
            )
        except User.DoesNotExist:
            message = "Cet utilisateur n'existe pas - Réessayez svp !"

    return render(request, 'subscription/subscribe_page.html', context={
        'form': form,
        'followers': followers,
        'followed_by': followed_by,
        'message': message
    })


@login_required
def delete_subscription(request, subscription_id):
    sub = get_object_or_404(UserFollows, id=subscription_id)
    if request.method == 'POST':
        sub.delete()
        return redirect('subscribe')

    return render(request, 'subscription/subscribe_page.html')
