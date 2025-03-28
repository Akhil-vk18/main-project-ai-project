from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import  *


urlpatterns = [
    path('add_hospital',views.add_hospital),
    path('vw_hospital',views.vw_hospital),
    path('delete_hospital/<int:id>/',views.delete_hospital),
    
    path('user_vw_hospitals',views.user_vw_hospitals),
   
]
