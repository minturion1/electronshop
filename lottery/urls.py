from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.lottery, name='lottery'),
    path('admin/', views.lottery_admin, name='lottery_admin'),
    path('admin-check/', views.admin_check, name='admin_check'),
    path('admin-check-success-ajax/<int:promocode_id>/', views.admin_check_success_ajax, name='admin_check_success_ajax'),
    path('add-promocode/',views.add_promocode, name='add_promocode'),
    path('add-promocode-ajax/', views.add_promocode_ajax, name='add_promocode_ajax'),
    path('success/<str:code>/',views.success,name='success_promo'),
]