from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('add_treatment', views.add_treatment),
    path('treatment_list',TreatmentList.as_view(),name='treatment_list'),
    path('edit_treatment/<int:id>/', EditTreatmentView.as_view(), name='edit_treatment'),
    path('delete_treatment/<int:id>/', views.delete_treatment, name='delete_treatment'),
    

]