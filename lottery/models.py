from django.db import models
from shop.models import Customer

# Create your models here.
class Promocode(models.Model):
    TYPES = (
        ('G', 'Green'),
        ('Y', 'Yellow'),
        ('R', 'Red'),
    )
    code = models.CharField(max_length=16, null=True, unique=True)
    type = models.CharField(max_length=1, choices=TYPES)
    gift = models.CharField(max_length=255, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    def empty(self):
        if self.gift == '0$':
            return True
        return False
    
    class Meta:
        verbose_name_plural = 'Promo codes'

class MyPromocode(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'My promo code {self.promocode.code}'
    
    class Meta:
        verbose_name_plural = 'My promo codes'
