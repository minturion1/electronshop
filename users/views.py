from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from shop.models import Customer
from referal.models import ReferalCode, Referal
from django.utils import timezone
import string
import random

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if not Customer.objects.filter(user=request.user).exists():
        customer = Customer.objects.create(user=request.user)
    customer = get_object_or_404(Customer, user=request.user)
    month_time = timezone.now().month - customer.created_time.month
    day_time = timezone.now().day - customer.created_time.day
    time = month_time + (day_time/30)
    if time<0.1:
        raiting=None
        deadline = 3-round(time*30)
    else:
        deadline=None
        raiting = ((customer.spent * customer.bought)/time)//5
        raiting=round(raiting)
    referal_code = get_object_or_404(ReferalCode, customer=customer).code

    context = {
        'raiting':raiting,
        'deadline':deadline,
        'customer':customer,
        'referal_code':referal_code,
    }
    return render(request, 'users/profile.html', context)
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, 'users/login.html', context)
@require_POST
def login_ajax(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                return JsonResponse({"message":"User not found"}, status=400)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                url = reverse("home")
                return JsonResponse({'message': 'Successful login', 'url': url}, status=200)
            else:
                return JsonResponse({'message': 'Incorrect username ot password'}, status=400)
        else:
            return JsonResponse({'message': 'Incorrect form'}, status=400)
    else:
        return JsonResponse({'message': 'Method is not allowed'}, status=405)
        

def generate_referral_code(length=12):
    characters = string.ascii_letters + string.digits
    referral_code = ''.join(random.choice(characters) for _ in range(length))
    return referral_code

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile'))
    form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)
@require_POST
def register_ajax(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data['first_name']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            invite_code = form.cleaned_data['invite_code']
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message":"Username is taken."}, status=400)
            if len(password1)<8:
                return JsonResponse({"message":"Password is to short"}, status=400)
            if not password1==password2:
                return JsonResponse({"message":"Passwords do not match"}, status=400)
            if invite_code:
                try:
                    code = get_object_or_404(ReferalCode, code=invite_code)
                    
                except:
                    return JsonResponse({"message":"Incorrect invite code"}, status=400)
            user = User.objects.create_user(username)
            if invite_code:
                code = get_object_or_404(ReferalCode, code=invite_code)
                referal = Referal()
                referal.commandor = code.customer.user
                referal.friend = user
                referal.save()
            user.first_name = first_name
            user.set_password(password1)
            user.save()
            
            customer = Customer(user=user)
            customer.save()
            referral_code = generate_referral_code()
            referal_c = ReferalCode()
            referal_c.customer = customer
            referal_c.code = referral_code
            referal_c.save()
            


            login(request, user)

            url = reverse('home')
            return JsonResponse({"message": "Successful registration", "url": url})
        else:
            return JsonResponse({'message': 'Error during registration'}, status=400)
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))