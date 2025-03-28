from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('ml_sym', home, name='home'),
    path('ml_symst', predict_disease_view, name='predict_disease_view'),
    
]
