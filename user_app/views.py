from django.contrib import messages
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from . models import *
from .forms import *
from .forms import UserRegisterForm, DoctorRegisterForm
from  django.core.files.storage import FileSystemStorage
import os

import secrets
import string
# from django.db.models import F, FloatField, ExpressionWrapper, Func
from django.views.generic import *
import geocoder

def index(request):
    doc=Register.objects.filter(usertype=2).count()
    print(doc)
    
    return render(request,'index.html',{'doc':doc})



def about(request):
    return render(request,'about.html')

def doLogin(request):
    form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, f"Username and password are required.", extra_tags='log')
            return render(request, 'login.html', {'form': form})

        # Check if the username exists in the database
        if not Register.objects.filter(username=username).exists():
            messages.error(request, f"This user is not registered. Please sign up first.", extra_tags='reg')
            return render(request, 'login.html', {'form': form})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, f"Invalid password. Please try again.", extra_tags='reg')
            return render(request, 'login.html', {'form': form})

        # Log the user in and set session data
        login(request, user)
        data = Register.objects.get(username=user)
        request.session['ut'] = data.usertype
        request.session['uid'] = data.id
        messages.success(request, f"Login Successful! Welcome {data.username}.", extra_tags='log')
        return redirect('/')

    return render(request, 'login.html', {'form': form}) 

def logout(request):
    auth.logout(request)
    return redirect('/') 

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if Register.objects.filter(email=email).exists():
                login_form = LoginForm()  
                messages.success(request, f'User Already Exist', extra_tags='log')
                return render(request, 'login.html', {'form': login_form, 'z': True})
            else:
                try:
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.usertype = 1
                    user.is_approved = True
                    user.save()
                    messages.success(request, f'Your registration has been successful! You can login now.', extra_tags='log')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        else:
            print(form.errors)
        return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
        title='User Register'
    return render(request, 'register.html', {'form': form,'title':'User Registration'})


def doctor_register(request):
    print("lkshdkjcabsdjhvbajdshv")
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST, request.FILES)
        print(form.errors)
        print(request.POST['username'])
        if form.is_valid():
            username = form.cleaned_data["username"]
            print(username, "uname")
            if Register.objects.filter(username=username).exists():
                login_form = LoginForm()  
                messages.success(request, 'Invalid username', extra_tags='log_dr')
                return render(request, 'login.html', {'form': login_form, 'z': True})
            email = form.cleaned_data["email"]
            if Register.objects.filter(email=email).exists():
                login_form = LoginForm()  
                return render(request, 'login.html', {'form': login_form, 'z': True})
            else:
                try:
                    user = form.save(commit=False)
                    user.password = make_password(form.cleaned_data['password'])
                    user.usertype = 2
                    user.is_approved = False
                    user.save()
                    form.save_m2m()
                    messages.success(request, 'Your registration has been successful! You can login only after admin approval.', extra_tags='log_dr')
                    return redirect('/login')
                except Exception as e:
                    form.add_error(None, f'An error occurred while saving the form: {e}')
        else:
            # Here, we're passing form.errors to the template when the form is invalid
            print(form.errors)
            messages.error(request, 'There were errors in your form. Please check the details and try again.')
        return render(request, 'register.html', {'form': form})
    else:
        form = DoctorRegisterForm()
        print(form.errors)
        title = 'Doctor Registration'
    return render(request, 'register.html', {'form': form, 'title': title})

def forgotpswd(request):
    return render(request, 'forgotpswd.html', {'user': request.user})

def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def reset_password(request):
    if request.method == "POST":

        user = Register.objects.get(username=request.POST['username'])
        print("USERSS",user)
        new_password = generate_random_password()
        user.password = make_password(new_password)
        print('Nesw Passworddddddddd',new_password)
        user.save()
        subject = 'password'
        message = "your password is " + str(new_password)
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [user.email]  
        send_mail(subject,message,email_from,recepient_list)
        messages.success(request, f'New Password is send to your registered email. Use it for login and change your password in your profile section. ', extra_tags='log')
               
    else:
        return render(request,"forgotpswd.html")
    return redirect('/login')



# def edit_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             # Check if the email is already in use by another user
#             if Register.objects.filter(email=email).exclude(id=request.user.id).exists():
#                 form.add_error('email', 'Email already exists')
#             else:
#                 try:
#                     user = form.save(commit=False)
#                     if form.cleaned_data.get('password'):
#                         user.password = make_password(form.cleaned_data['password'])
#                     user.save()

#                     # Update the session with the new user data
#                     update_session_auth_hash(request, user)

#                     messages.success(request, 'Profile updated successfully.',extra_tags='log')
#                     return redirect('/profile')
#                 except Exception as e:
#                     form.add_error(None, f'An error occurred while updating the profile: {e}')
#         else:
#             messages.error(request, 'Please correct the errors below.', extra_tags='log')
#     else:
#         initial_data = {
#             'username': request.user.username,
#             'email': request.user.email,
#             'place': request.user.place,
#             'phone': request.user.phone,
#             'image': request.user.image
#         }
#         form = ProfileForm(initial=initial_data, instance=request.user)
    
#     return render(request, 'update_form.html', {'form': form})



@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        if user.usertype == 2:
            form = DRProfileForm(request.POST, request.FILES, instance=user)
        else:
            form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                updated_user = form.save(commit=False)
                if form.cleaned_data.get('password'):
                    updated_user.password = make_password(form.cleaned_data['password'])
                updated_user.save()

                # Update session with new user data
                update_session_auth_hash(request, updated_user)

                messages.success(request, 'Profile updated successfully.', extra_tags='log')
                return redirect('/profile')
            except Exception as e:
                form.add_error(None, f'An error occurred while updating the profile: {e}')
        else:
            print(form.errors)
            messages.error(request, 'Please correct the errors below.', extra_tags='log')
    else:
        # Populate initial data
        form = DRProfileForm(instance=user) if user.usertype == 2 else ProfileForm(instance=user)

    return render(request, 'update_form.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        print("POST request received.")
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("Form is valid.")
            try:
                user = form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, 'Your password has been changed successfully.', extra_tags='log')
                return redirect('/login')
            except Exception as e:
                print(f"Error saving form: {e}")
                messages.error(request, 'An error occurred. Please try again.', extra_tags='log')
        else:
            # Debugging: print form errors
            print("Form is not valid.")
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the error below.', extra_tags='log')
    else:
        print("GET request received.")
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'password_change_form.html', {'form': form})



class UpdateLocationView(View):
    def get(self, request, id):
        user = Register.objects.get(id=id) 
        g = geocoder.ip('me')
        user.lat = g.latlng[0] 
        user.long = g.latlng[1] 
        user.save()
        messages.success(request,'Updated Your location successfully',extra_tags='user_reg')
        return redirect('/')








@login_required
def delete_account(request):
    user= request.user
    try:
        account = Register.objects.get(id=user.id)
        auth.logout(request)
        account.delete()
        return redirect('/')  # Redirect to the home page
    except Register.DoesNotExist:
        return redirect('/')

@login_required
def delete_user(request,id):
    try:
        account = Register.objects.get(id=id)
        account.delete()
        return redirect('/')  # Redirect to the home page
    except Register.DoesNotExist:
        return redirect('/')
