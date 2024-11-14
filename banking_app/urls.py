from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),
    path('accounts/create_account/', views.create_account, name='create_account'),
    path('accounts/deposit/<int:account_id>/', views.deposit, name='deposit'),
    path('accounts/withdraw/<int:account_id>/', views.withdraw, name='withdraw'),
    path('accounts/login/', views.login, name='login'),
    path('', views.home, name='home'),
    #path('accounts/logout/', views.logout, name='logout'),
]