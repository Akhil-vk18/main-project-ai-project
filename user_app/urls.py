from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import  *



urlpatterns = [
    path('',views.index),
    path('login',views.doLogin),
    path('about',views.about,name='about'),
    path('user_register', views.user_register, name='user_register'),
    path('doctor_register',views.doctor_register,name='doctor_register'),
    path('forgotpswd/',views.forgotpswd),
    path('logout',views.logout),
    path('generate_random_password',views.generate_random_password),
    path('change_password',views.change_password,name='change_password'),
    path('reset_password',views.reset_password,name='password_change'),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('u_location/<int:id>', UpdateLocationView.as_view(), name='update_location'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
