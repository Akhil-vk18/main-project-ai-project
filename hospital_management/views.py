from django.shortcuts import render,redirect
from admin_app.models import *
# Create your views here.
from user_app.models import *
from user_app.forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from geopy.distance import geodesic
import geocoder

def add_hospital(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Register.objects.filter(email=email).exists():
                login_form = LoginForm()  
                return render(request, 'vw_.html', {'form': login_form, 'z': True})
            else:
                try:
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.usertype = 3
                    user.is_approved = False
                    user.save()
                    messages.success(request, 'Your registration has been successful! ', extra_tags='log_dr')
                    return redirect('/vw_hospital')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        return render(request, 'add_hospital.html', {'form': form})
    else:
        form = UserRegisterForm()
        title='Add Hospital'
    return render(request, 'add_hospital.html', {'form': form,'title':title})




def vw_hospital(request):
    hospitals = Register.objects.filter(usertype=3)  # Fetch all hospital records
    print(hospitals)
    context = {
        'hospitals': hospitals,  # Pass hospital data to the template
    }
    return render(request, 'vw_hospital.html', context)




def user_vw_hospitals(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': 'Please log in to view nearby hospitals.'})

    # Get the user's current location using IP
    g = geocoder.ip('me')
    if g.latlng:
        user_lat, user_long = g.latlng
    else:
        user_lat, user_long = 0, 0
    user_coords = (user_lat, user_long)

    # Get all hospitals with latitude and longitude
    hospitals = Register.objects.filter(usertype=3)
    print(hospitals)
    # Calculate distances for each hospital
    for hospital in hospitals:
        if hospital.lat and hospital.long:
            hospital_coords = (hospital.lat, hospital.long)
            distance = geodesic(user_coords, hospital_coords).km
            hospital.dis = round(distance, 2)  # Add a `dis` attribute dynamically
        else:
            hospital.dis = float('inf')

    # Sort hospitals by distance
    sorted_hospitals = sorted(hospitals, key=lambda hospital: hospital.dis)

    context = {'nearby_hospitals': sorted_hospitals}
    return render(request, 'user_vw_hospitals.html', context)






def delete_hospital(request,id):
    hos_id=Register.objects.get(id=id)
    hos_id.delete()
    return redirect('/vw_hospital')