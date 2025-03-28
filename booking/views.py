from django.shortcuts import render,redirect

# Create your views here.
from .forms import *
from user_app.models import *
import geopy
import geocoder
from geopy.distance import geodesic
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib import messages
from .models import *
from feedback.models import *


from django.http import HttpResponse, Http404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from io import BytesIO
from django.shortcuts import get_object_or_404




def add_working_time(request):
    # Create a formset for the DutyTime model with 1 extra form
    OperatingTimeFormSet = modelformset_factory(DutyTime, form=OperatingTimeForm, extra=1)

    if request.method == 'POST':
        formset = OperatingTimeFormSet(request.POST)
        
        if formset.is_valid():
            # Get the logged-in doctor instance
            doctor = Register.objects.get(id=request.user.id)
            existing_times = DutyTime.objects.filter(doctor=doctor)  # Fetch current times for this doctor
            
            instances = formset.save(commit=False)
            added_times = []  # Track new valid working times

            for instance in instances:
                # Check if morning time is repeated
                morning_exists = existing_times.filter(morning_start=instance.morning_start).exists()
                # Check if evening time is repeated
                evening_exists = existing_times.filter(evening_start=instance.evening_start).exists()
                # Check if both morning and evening times are repeated together
                combined_exists = existing_times.filter(morning_start=instance.morning_start, evening_start=instance.evening_start).exists()
                
                # If no time is repeated, save the instance
                if not morning_exists and not evening_exists and not combined_exists:
                    instance.doctor = doctor
                    instance.save()
                    added_times.append(instance)
                else:
                    # Optionally, handle feedback for each case if needed
                    if morning_exists:
                        messages.warning(request, f"Morning time {instance.morning_start} is already added.", extra_tags='log')
                    if evening_exists:
                        messages.warning(request, f"Evening time {instance.evening_start} is already added.", extra_tags='log')
                    if combined_exists:
                        messages.warning(request, f"Time slot from {instance.morning_start} to {instance.evening_start} is already added.", extra_tags='log')
            
            if added_times:
                messages.success(request, "Working times saved successfully!", extra_tags='log')
            else:
                messages.info(request, "No new working times were added. Duplicate times were ignored.", extra_tags='log')
                
            return redirect('/vw_timing')  # Redirect after successful form submission
        else:
            messages.error(request, "There was an error with your submission.")
    
    else:
        formset = OperatingTimeFormSet(queryset=DutyTime.objects.none())  # Load empty formset

    # Context with formset and title for the template
    context = {
        'formset': formset,
        'title': 'Operating Time'
    }
    return render(request, 'working_time.html', context)



def vw_timing(request):
    existing_timings = DutyTime.objects.filter(doctor=request.user)

    
    return render(request, 'vw_timing.html', {'existing_timings': existing_timings})



def edit_timing(request, timing_id):
    timing = DutyTime.objects.get(id=timing_id)
    if request.method == 'POST':
        form = OperatingTimeForm(request.POST, instance=timing)
        if form.is_valid():
            form.save()
            return redirect('/vw_timing')
    else:
        form = OperatingTimeForm(instance=timing)
    return render(request, 'edit_time.html', {'form': form, 'timing': timing})  # Pass 'form' not 'formset'



def delete_timing(request, timing_id):
    timing = DutyTime.objects.get(id=timing_id)
    timing.delete()
    return redirect('/vw_timing')


class ViewDoc(ListView):
    model = Register
    template_name = 'vw_doc.html'
    context_object_name = 'mymodels'

    def get_queryset(self):
        current_user = self.request.user
        search_query = self.request.GET.get('q', '')
        # Filter approved restaurants
        approved_users = Register.objects.filter(usertype=2, is_approved=True)
        if search_query:
            # Filter based on search query
            approved_users = approved_users.filter(
                Q(username__icontains=search_query) |
                Q(place__icontains=search_query) |
                Q(phone__icontains=search_query) 
                
             
            )
            
        if current_user.usertype == 1:
            # Get the current user's location using IP
            g = geocoder.ip('me')
            if g.latlng:
                lat, long = g.latlng
            else:
                lat, long = 0, 0
            coords_1 = (lat, long)

            # Calculate distance for each restaurant
            for user in approved_users:
                if user.lat and user.long:
                    coords_2 = (user.lat, user.long)
                    distance = geodesic(coords_1, coords_2).km
                    user.dis = round(distance, 2)
                    print(user.dis)
                else:
                    user.dis = float('inf')
                    print(user.dis)
            # Sort restaurants by distance
            sorted_users = sorted(approved_users, key=lambda user: user.dis)
            return sorted_users
        else:
            
            return approved_users
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['search_query'] = self.request.GET.get('q', '')
        context['feedbacks'] = Feedback.objects.all().select_related('booking_id__dr_id', 'user_id')
        return context
    
    
    
    
def doc_details(request, id):
    doc_dtls = Register.objects.get(id=id)
    current_user = request.user

    # Calculate distance if usertype is 1
    if current_user.usertype == 1:
        g = geocoder.ip('me')
        if g.latlng:
            lat, long = g.latlng
        else:
            lat, long = 0, 0
        coords_1 = (lat, long)

        if doc_dtls.lat and doc_dtls.long:
            coords_2 = (doc_dtls.lat, doc_dtls.long)
            distance = geodesic(coords_1, coords_2).km
            doc_dtls.dis = round(distance, 2)
        else:
            doc_dtls.dis = float('inf')

    # Retrieve feedbacks for the doctor
    feedbacks = Feedback.objects.filter(booking_id__dr_id=doc_dtls).select_related('user_id')

    return render(request, 'vw_doc_details.html', {
        'doc': doc_dtls,
        'dis': doc_dtls.dis,
        'feedbacks': feedbacks
    })
    
def book_appointment(request, doctor_id):
    doctor = Register.objects.get(id=doctor_id)
    duty_times = doctor.duty_times.all()  # Get all duty timings for this doctor

    if request.method == 'POST':
        booking_time = request.POST.get('duty_time')
        booking_date = request.POST.get('book_date')
        user = Register.objects.get(id=request.user.id)

        # Check if the selected date and time are already booked
        # if Book_Dr.objects.filter(dr_id=doctor, booking_date=booking_date, booking_time=booking_time).exists():
        #     messages.error(request, "This appointment time is already booked. Please choose another time.",extra_tags='book')
        # else:
        Book_Dr.objects.create(
            dr_id=doctor,
            booking_time=booking_time,
            booking_date=booking_date,
            user_id=user
        )
        messages.success(request, "Your appointment has been successfully booked.",extra_tags='booked')
        return redirect('/vw_booking/') 

    return render(request, 'book.html', {
        'doctor': doctor,
        'duty_times': duty_times,
    })
    



    
from datetime import date, datetime

def view_bookings(request):
    bookings = Book_Dr.objects.filter(user_id=request.user)

    # Convert booking_date to a date object and check cancellable condition
    for booking in bookings:
        try:
            # Convert string to date object
            booking_date = datetime.strptime(booking.booking_date, "%Y-%m-%d").date()
            booking.booking_date_object = booking_date  # Add as an attribute for template use
        except ValueError:
            # Handle invalid date format gracefully
            booking.booking_date_object = None

        # Determine if the booking is cancellable
        booking.is_cancellable = (
            booking.c_status != "cancelled" and booking_date >= date.today()
        )

    context = {
        'bookings': bookings,
        'today': date.today(),  # Pass today's date to the template
    }
    return render(request, 'vw_bookings.html', context)




def view_bookings_dr(request):
    # Fetch all bookings made by the logged-in user
    bookings = Book_Dr.objects.filter(dr_id=request.user)
    print(bookings)
    context = {
        'bookings_dr': bookings
    }
    
    return render(request, 'vw_bookings.html', context)


 # Replace with the correct import for your model

def download_appointment_pdf(request, booking_id):

    # Fetch booking details
    try:
        booking = get_object_or_404(Book_Dr, id=booking_id)
    except Book_Dr.DoesNotExist:
        raise Http404("Booking not found.")

    # Prepare the PDF buffer and canvas
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Colors and fonts
    background_color = HexColor("#E3F2FD")  # Light blue background
    text_color = HexColor("#0D47A1")  # Dark blue text
    heading_color = HexColor("#1565C0")  # Slightly lighter blue for headings

    # Draw background
    pdf.setFillColor(background_color)
    pdf.rect(0, 0, 612, 792, fill=True, stroke=False)  # Fill the whole page

    # Set up styles
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(heading_color)
    pdf.drawString(100, 750, "Appointment Details")  # Title

    # Appointment Details Section
    pdf.setFont("Helvetica", 14)
    pdf.setFillColor(text_color)
    pdf.drawString(100, 720, f"Doctor: {booking.dr_id.username}")
    pdf.drawString(100, 690, f"Date: {booking.booking_date}")
    pdf.drawString(100, 660, f"Time: {booking.booking_time}")
    pdf.drawString(100, 630, f"Booking ID: {booking.id}")
    pdf.drawString(100, 600, "Thank you for choosing our service!")

    # Footer Section
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.setFillColor(HexColor("#546E7A"))  # Grey-blue footer text
    pdf.drawString(100, 50, "This is a system-generated document. No signature is required.")

    # Finalize and save the PDF
    pdf.save()
    buffer.seek(0)

    # Build the HTTP response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=appointment_{booking_id}.pdf'

    return response






def cancel_booking(request,id):
    book_id = Book_Dr.objects.get(id=id)
    print(book_id,"dd")
    book_id.c_status = "cancelled"
    book_id.save()
    return redirect('view_bookings')