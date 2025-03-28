from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('add_disease', views.add_disease),
    path('disease_list',DiseaseListView.as_view(),name='disease_list'),
    path('edit_disease/<int:pk>/', views.edit_disease_view, name='edit_disease'),
    path('delete_disease/<int:id>/', views.delete_disease, name='delete_disease'),
    

]