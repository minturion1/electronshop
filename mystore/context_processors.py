from django.shortcuts import get_object_or_404
from shop.models import *



def customer(request):
    try:
        customer = get_object_or_404(Customer, user=request.user)
    except:
        customer=None
    return {'customer_info':customer}
