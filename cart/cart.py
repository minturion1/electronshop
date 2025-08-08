from decimal import Decimal
from django.conf import settings
from shop.models import Product
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, currency=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            # Перевіряємо валюту і встановлюємо відповідну ціну
            price = product.get_points() if currency == '2' else product.price
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(price),
                                    'currency': currency}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        total_price_decimal = Decimal(0)
        for item in cart.values():
            product = item.get('product')
            if product and product.discount:
                price = product.discount_price()
            else:
                price = Decimal(item['price'])
            item['price'] = price  # Встановлюємо ціну для item
            total_price_decimal += price * item['quantity']  # Обчислюємо total_price
            item['total_price'] = price * item['quantity']
            yield item
        self.total_price = total_price_decimal

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):

        total_price = 0
        for item in self.cart.values():
            
            quantity = item['quantity']
            if  item['currency'] == '1':
                product = item.get('product')
                if product and product.discount:
                    price = product.discount_price()
                else:
                    price = Decimal(item['price'])
                total_price += price * quantity
        return total_price
    
    
    def get_total_points(self):

        total_price = 0
        for item in self.cart.values():
            
            quantity = item['quantity']
            if item['currency'] == '2':
                price = Decimal(item['price'])
                total_price += price * quantity
        return total_price
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save() 