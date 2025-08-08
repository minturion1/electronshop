from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import decimal
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    points = models.PositiveIntegerField(default=200, null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    spent = models.IntegerField(default=0,null=True)
    bought = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Customers'

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, verbose_name=u"Category name")
    img = models.ImageField(upload_to='photos/', null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('subcategories', args=[str(self.slug)])
    
    class Meta:
        verbose_name_plural = 'Categories'

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, verbose_name=u'Subcategory name')
    img = models.ImageField(upload_to='shop/photos/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('products', args=[str(self.slug)])

    class Meta:
        verbose_name_plural = 'Subcategories'

class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, verbose_name =u"Product name")
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    available = models.BooleanField(default=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    img = models.ImageField(upload_to='products/%Y/%m/%d',blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(null=True)
    slug = models.SlugField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True,null=True)

    

    def __str__(self):
        return self.name
    

    def get_points(self):
        return round(self.price * 25)
    def discount_price(self):
        discounted_price = self.price - self.price * self.discount/100
        return discounted_price
    
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

class DeviceFeature(models.Model):
    device = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="features", verbose_name="Пристрій")
    feature_name = models.CharField(max_length=255, verbose_name="Characteristics")
    feature_value = models.CharField(max_length=255, verbose_name="Value")

    def __str__(self):
        return f"{self.device.name} - {self.feature_name}: {self.feature_value}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    note = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    paid = models.BooleanField(default=False)
    old = models.BooleanField(default=False)


    def __str__(self):
        if self.customer:
            return f'Order from customer {self.customer.user.first_name} ({self.customer.user.username})'
        else:
            return f'Order without customer (ID: {self.id})'
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name_plural = 'Orders'
    def get_total_cost(self):
        total_price = 0
        for item in self.items.all():
            if item.currency == 1:
                total_price += item.price * item.quantity
        return total_price
    
    def get_total_points(self):
        total_points = 0
        for item in self.items.all():
            if item.currency == 2: 
                total_points += round(item.price) * item.quantity
        return total_points
    
class OrderItem(models.Model):
    class Currency(models.IntegerChoices):
        GRIVNA = 1, 'Dollar'
        COINS = 2, 'Point'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)

    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)
    currency = models.IntegerField(choices=Currency.choices, default=Currency.GRIVNA, null=True)
    old = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    def get_cost(self):
        if self.currency == 2:
            return round(self.price) * self.quantity
        return self.price * self.quantity
