from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-page-view'),
    path('login', views.LoginView.as_view(), name='user-login'),
    path('logout', views.logoutView, name='user-logout')
    ]
