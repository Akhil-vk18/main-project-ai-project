from django.shortcuts import render,redirect
from booking.models import Book_Dr
from booking.models import *
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
# Create your views here.
def feedback_list(request,id):
    try:
        feedbacks = Feedback.objects.get(booking_id=id)
        print(feedbacks)
    except Feedback.DoesNotExist:
        print("hi")
        feedbacks=None
    return render(request, 'vw_feedback.html', {'feedback': feedbacks})

def add_feedback(request, booking_id):
    booking = Book_Dr.objects.get(id=booking_id)
    user = request.user  # Assuming you use Django's authentication system
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.booking_id = booking
            feedback.user_id = user
            feedback.created_at = timezone.now()
            booking.f_status="feedbacked"
            booking.save()
            feedback.save()
            return redirect('/vw_booking/')
        else:
            print(form.errors)
    else:
        form = FeedbackForm()
    return render(request, 'add_feedback.html', {'form': form, 'booking': booking})

def others_feedback(request, id):
    # Get the doctor's feedback based on the doctor ID
    feedbacks = Feedback.objects.filter(booking_id__dr_id=id)  # Fetch all feedbacks for the doctor
    print(feedbacks)
    doctor = get_object_or_404(Book_Dr, id=id)  # Fetch the doctor by ID
    print(doctor)
    return render(request, 'vw_feedback.html', {'feedbacks': feedbacks, 'doctor': doctor})