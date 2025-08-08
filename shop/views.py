from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.cart import Cart
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm
from referal.models import Referal
from .forms import OrderCreateForm
from django.utils import timezone
from datetime import timedelta


def full_assortment(request):
    products = Product.objects.filter(available=True)
    items_per_page = 20

    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        
        products = paginator.page(1)
    except EmptyPage:
        
        products = paginator.page(paginator.num_pages)
    context = {
        'products':products,
    }
    return render(request, 'shop/full_assortment.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    return render(request, 'shop/categories.html', context)

def subcategories(request, cat_slug):
    subcategories = Subcategory.objects.filter(category__slug=cat_slug)
    category = get_object_or_404(Category, slug=cat_slug)
    context = {
        "subcategories":subcategories,
        'category':category,
    }
    return render(request, 'shop/subcategories.html', context)

def products(request, cat_slug, subcat_slug):
    products = Product.objects.filter(subcategory__slug=subcat_slug)
    category = get_object_or_404(Category, slug=cat_slug)
    subcategory = get_object_or_404(Subcategory, slug=subcat_slug)
    context = {
        'products':products,
        'category': category,
        'subcategory':subcategory,
    }
    return render(request, 'shop/products.html', context)

def product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    chars = DeviceFeature.objects.filter(device__id=product.id)
    print(chars)
    subcategory = product.subcategory
    try:
        subcategory = get_object_or_404(Subcategory, slug=subcategory.slug)
        category = product.subcategory.category
        category = get_object_or_404(Category, slug=category.slug)
    except:
        subcategory = None
        category = None
    
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    product_id_str = str(product.id)
    context = {
        'product':product,
        'category': category,
        'subcategory':subcategory,
        'cart_product_form': cart_product_form,
        'cart':cart,
        'product_id_str':product_id_str,
        'chars':chars,

    }
    return render(request, 'shop/product.html', context)

def my_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    my_orders = Order.objects.filter(customer__user=request.user, old=False).order_by('-created')
    my_old_orders = Order.objects.filter(customer__user=request.user, old=True).order_by('-created')
    context = {
        'my_orders':my_orders,
        'my_old_orders':my_old_orders,
    }
    return render(request, 'shop/my_orders.html', context)

def my_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order.get_total_cost())
    order_items = OrderItem.objects.filter(order__id=order_id)
    context = {
        'order':order,
        "order_items":order_items,
    }
    return render(request, 'shop/my_order_detail.html', context)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    context = {
        'order':order,
    }
    return render(request, 'shop/delete_order.html', context)
@require_POST
def delete_order_ajax(request, order_id):
    if request.method=='POST':
        order = get_object_or_404(Order, id=order_id, customer__user=request.user)
        order.delete()
        return JsonResponse({'message':'Order canceled'})
@require_POST
def add_to_cart_ajax(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    


    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'message':'Log in to your profile'}, status=400)

        count = request.POST.get('count')
        currency = request.POST.get('currency')
        
        count = int(count)  
        
        customer = get_object_or_404(Customer, user=request.user)
        if product.count==0:
            return JsonResponse({'message':'Not available'}, status=400)
        if count == 0:
            return JsonResponse({'message':'Please specify the quantity of goods'}, status=400)
        try:
            product = Product.objects.get(id=product_id)
            
        except:
            return JsonResponse({'message':'Product not found'}, status=400)
        if currency == '2':
            if customer.points< ((count*product.get_points())+cart.get_total_points()):
                return JsonResponse({'message':f'Not enough points. Need {(count*int(product.get_points())+int(cart.get_total_points()))-customer.points} more.'}, status=400)
        customer = get_object_or_404(Customer, user=request.user)
        
        cart.add(product=product, quantity=count, currency=currency, override_quantity=True)
            
            
        return JsonResponse({'message': 'Added to cart'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
@require_POST
def delete_cart_ajax(request, cart_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=cart_id)
    cart.remove(product)
    return JsonResponse({'message': 'Object deleted successfully'})

def order_create(request):
    cart = Cart(request)
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'],
                                        currency=item['currency'],)
                


            context = {
                'order':order,
            }
            html_content = render_to_string('shop/mail.html', context)
            subject = f"New order!"
            message = ''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['minturion@gmail.com']
            send_mail(subject, message , email_from ,recipient_list, html_message=html_content, fail_silently=True)





            cart.clear()
            current_time = timezone.now()


            new_time = current_time + timedelta(minutes=5)
            return render(request,
            'shop/order/created.html',
            {'order': order, 'time':new_time})
    else:
        form = OrderCreateForm()
    return render(request,
        'shop/order/create.html',
        {'cart': cart, 'form': form})


def actions(request):
    products = Product.objects.filter(discount__gt=0)
    items_per_page = 20

    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        
        products = paginator.page(1)
    except EmptyPage:
        
        products = paginator.page(paginator.num_pages)
    context = {
        'products':products,
    }
    return render(request, 'shop/actions.html', context)






def admin_orders(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('my_orders'))
    orders = Order.objects.filter(old=False).order_by('-created')
    context = {
        'orders':orders,
    }
    return render(request, 'shop/admin_orders.html', context)

def admin_order_detail(request, order_id):
    
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('my_orders'))
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_points=0
    context = {
        'order':order,
        'order_items':order_items,
        'total_points':total_points,
    }
    return render(request, 'shop/admin_order_detail.html', context)
@require_POST
def admin_order_reject(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    order_items.delete()
    order.delete()

    return JsonResponse({'message': 'Order rejected and deleted'})
@require_POST
def admin_order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customer=order.customer
    order_items = OrderItem.objects.filter(order=order)

    for order_item in order_items:
        product = order_item.product
        product.count -= order_item.quantity
        product.save()

        customer.bought += 1
    customer.spent = round(order.get_total_cost())
    customer.points-=order.get_total_points()
    customer.points += order.get_total_cost()

    if Referal.objects.filter(friend = request.user).exists():
        
        commandor = get_object_or_404(Referal, friend = request.user).commandor
        commandor_customer = get_object_or_404(Customer, user__id = commandor.id)
        commandor_customer.points += order.get_total_cost()//10

        commandor_customer.save()

    customer.save()
    order_items.update(old=True)
    order.old=True
    order.save()
    

    return JsonResponse({'message': 'Order completed'})


