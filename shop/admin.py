from django.contrib import admin
from .models import Product, DeviceFeature, Order, OrderItem, Category, Subcategory, Customer

class DeviceFeatureInline(admin.TabularInline):
    model = DeviceFeature
    extra = 10  

@admin.register(DeviceFeature)
class DeviceFeatureAdmin(admin.ModelAdmin):
    list_display = ['device', 'feature_name', 'feature_value']
    list_filter = ['device']
    search_fields = ['feature_name', 'feature_value', 'device__name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [DeviceFeatureInline]
    list_display = ['slug', 'name', 'price', 'available', 'count', 'created', 'updated', 'discount']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['name', 'price', 'available', 'count', 'discount']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'contact', 'paid', 'old', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user',)
