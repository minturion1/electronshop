from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import *
from django.views.decorators.http import require_POST
import random
import string
from django.shortcuts import get_object_or_404
# Create your views here.

def generate_promo_code(length=10):
    characters = string.ascii_letters + string.digits
    promo_code = ''.join(random.choice(characters) for _ in range(length))
    return promo_code

def lottery_admin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = AddPromocodeForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            type = form.cleaned_data['type']
            if type == 'G':
                fond = (10*count)//2
                gift_options = [5, 10, 20, 30, 40, 50]
            if type == 'Y':
                fond = (20*count)//2
                gift_options = [10, 20, 40, 60, 80, 100]
            if type == 'R':
                fond = (50*count)//2
                gift_options = [20, 40, 50, 70, 100, 200]

            for i in range(1, count+1):
                gift = random.choice(gift_options)
                fond -= gift
                if fond <=0:
                    gift=0
                
                


                promo = generate_promo_code()
                promocode = Promocode()
                promocode.code = promo
                promocode.type = type
                promocode.gift = f'{gift}$'
                promocode.save()


    else:
        form = AddPromocodeForm()
    context = {
        'form':form
    }
    return render(request, 'lottery/admin.html', context)



def lottery(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    my_promocodes = MyPromocode.objects.filter(customer__user=request.user)
    context = {
        'my_promocodes':my_promocodes,
    }
    return render(request, 'lottery/lottery.html', context)

def add_promocode(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    form = PromocodeForm()
    context = {
        "form": form,
    }
    return render(request, 'lottery/add.html', context)

@require_POST
def add_promocode_ajax(request):
    if request.method == 'POST':
        form = PromocodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if MyPromocode.objects.filter(promocode__code=code).exists():
                return JsonResponse({"message":"Someone has already entered this promo code"}, status=400)
            if not Promocode.objects.filter(code=code).exists():
                return JsonResponse({"message":"Incorrect promo code"}, status=400)
            
            my_promo = MyPromocode()
            my_promo.customer = get_object_or_404(Customer, user=request.user)
            my_promo.promocode = get_object_or_404(Promocode, code=code)
            my_promo.save()
            url = reverse("success_promo", args=[code])
            return JsonResponse({'message': 'Successful', 'url': url}, status=200)
        else:
            return JsonResponse({'message': 'Incorrect promo code'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    

def success(request, code):
    promocode = get_object_or_404(MyPromocode, promocode__code = code, customer__user=request.user)
    defeat=False
    promocode = promocode.promocode
    if promocode.gift == '0$':
        defeat=True
    
    context = {
        'promocode':promocode,
        'defeat':defeat,
    }
    return render(request, 'lottery/success.html', context)





def admin_check(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = CheckPromocodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                promocode = get_object_or_404(Promocode, code=code)
                try:
                    my_promocode = get_object_or_404(MyPromocode, promocode__id=promocode.id)
                except:
                    my_promocode = None
            except:
                promocode='None'
                my_promocode = None
            

    else:
        form = CheckPromocodeForm()
        promocode = None
        my_promocode = None
    context = {
        'form':form,
        'promocode':promocode,
        'my_promocode':my_promocode,
    }
    return render(request, 'lottery/admin_check.html', context)

@require_POST
def admin_check_success_ajax(request, promocode_id):
    try:
        promocode = get_object_or_404(Promocode, id=promocode_id)
    except:
        return JsonResponse({'message': 'Error'}, status=400)
    promocode.active = False
    promocode.save()

    return JsonResponse({'message': 'Payment sent'})
