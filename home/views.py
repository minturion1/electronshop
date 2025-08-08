from django.shortcuts import render
from shop.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from shop.models import *

# Create your views here.
def home(request):
    categories = Category.objects.all()
    actions = Product.objects.filter(discount__gt=0, available=True)[:20]
    promocodes_green = Product.objects.filter(slug='loterejnij-promokod-zelenij')
    promocodes_yellow = Product.objects.filter(slug='loterejnij-promokod-zhovtij')
    promocodes_red = Product.objects.filter(slug='loterejnij-promokod-chervonij')
    promocodes = promocodes_yellow | promocodes_green | promocodes_red
    promocodes=promocodes.order_by('price')
    context = {
        'categories':categories,
        'actions':actions,
        'promocodes':promocodes
    }
    return render(request, 'home/home.html', context)


