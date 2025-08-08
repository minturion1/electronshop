from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('full-assortment/', views.full_assortment, name='full_assortment'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-order-detail/<int:order_id>', views.my_order_detail, name='my_order_detail'),
    path('add-to-cart-ajax/<int:product_id>', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('delete-cart-ajax/<int:cart_id>/', views.delete_cart_ajax, name='delete_cart_ajax'),
    path('delete-order/<int:order_id>', views.delete_order, name='delete_order'),
    path('delete-order-ajax/<int:order_id>/', views.delete_order_ajax, name='delete_order_ajax'),
    path('create-order/', views.order_create, name='order_create'),

    path('actions/', views.actions, name='actions'),

    path('categories/', views.categories, name='categories'),
    path('<slug:cat_slug>', views.subcategories, name='subcategories'),
    path('<slug:cat_slug>/<slug:subcat_slug>', views.products, name='products'),
    path('product/<slug:product_slug>/buy', views.product, name='product'),



    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order-detail/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-order-reject-ajax/<int:order_id>/', views.admin_order_reject, name='admin_order_reject_ajax'),
    path('admin-order-confirm-ajax/<int:order_id>/', views.admin_order_confirm, name='admin_order_confirm_ajax'),
]