from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *
# from .views import YourModelListView


urlpatterns = [
    path('vw_doc',views.ViewDoc.as_view()),
    path('vw_doc_details/<int:id>/',views.doc_details),
    path('add_working_time',views.add_working_time),
    path('vw_timing',views.vw_timing),
    path('timing/<int:timing_id>/edit/', edit_timing, name='edit_timing'),
    path('timing/<int:timing_id>/delete/', delete_timing, name='delete_timing'),
    path('book_appointment/<int:doctor_id>/', book_appointment, name='book_appointment'),
    path('vw_booking/', view_bookings, name='view_bookings'),
    path('vw_booking_dr/', view_bookings_dr, name='view_bookings_dr'),
    path('cancel_booking/<int:id>/', cancel_booking, name='cancel_booking'),
    path('download_appointment_pdf/<int:booking_id>/', views.download_appointment_pdf, name='download_appointment_pdf'),
   
    
]
