from django.db import models
from django.contrib.auth.models import User
from shop.models import Customer
import random
import string
# Create your models here.


class ReferalCode(models.Model):
    customer = models.ForeignKey(Customer, related_name='referal_customer', on_delete=models.CASCADE,null=True)
    code = models.CharField(max_length=12,null=True)

    def __str__(self):
        return f'{self.code} - {self.customer.user.username}'

class Referal(models.Model):
    commandor = models.ForeignKey(User, related_name='issued_referals', on_delete=models.CASCADE, null=True, blank=True)
    friend = models.ForeignKey(User, related_name='received_referals', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Friendship {self.commandor.username} and {self.friend.username}'