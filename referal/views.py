from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404

# Create your views here.

def referal_list(request):
    my_friends_commandor = Referal.objects.filter(commandor=request.user)
    my_friends_friend = Referal.objects.filter(friend=request.user)
    my_friends = my_friends_commandor | my_friends_friend
    invite_code = get_object_or_404(ReferalCode, customer__user=request.user)
    context = {
        'my_friends':my_friends,
        'invite_code':invite_code,
    }
    return render(request, 'referal/list.html', context)
