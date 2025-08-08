from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('referal_list/', views.referal_list, name='referal_list'),
]