from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'type', 'gift','active']
    list_filter = ['type', 'gift', 'active']

@admin.register(MyPromocode)
class MyPromocodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'promocode', 'time']
    list_filter = ['customer','promocode']