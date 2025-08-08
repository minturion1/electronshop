from django.urls import path
from .import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('login-ajax/', views.login_ajax, name='login-ajax'),
    path('register/', views.register, name='register'),
    path('register-ajax/', views.register_ajax, name='register-ajax'),
]
