from django.urls import path
from . import views

urlpatterns = [
    path('vw_feedback/<int:id>/', views.feedback_list, name='feedback_list'),
    path('feedback_add/<int:booking_id>/', views.add_feedback, name='add_feedback'),
    path('others_feedback/<int:id>/', views.others_feedback, name='others_feedback'),
]
