# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_account/', views.create_account, name='create_account'),
    path('deposit/<int:account_id>/', views.deposit, name='deposit'),
    path('withdraw/<int:account_id>/', views.withdraw, name='withdraw'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]