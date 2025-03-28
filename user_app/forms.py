from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from PIL import Image



class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    place = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'})
    )
    phone = forms.CharField(
        max_length=10,  
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'})
    )
    image = forms.ImageField(
        required=False,  # Making the image field optional
        label="Profile Photo",  # Updating the label to "Profile Photo"
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        help_text="Max size: 2 MB. Max dimensions: 800x800 pixels."  # Adding help text
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Open the image file
            img = Image.open(image)
            
            # Specify your required dimensions
            max_width = 800
            max_height = 800

            # Check dimensions
            if img.width > max_width or img.height > max_height:
                raise forms.ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.")

            # Optional: Check file size
            max_file_size = 2 * 1024 * 1024  # 2 MB
            if image.size > max_file_size:
                raise forms.ValidationError("Image file size should not exceed 2 MB.")

        return image
    
    COUNTRY_CHOICES = [
        ('', 'country*'),
        ('Afghanistan', 'Afghanistan'),
        ('Armenia', 'Armenia'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Cambodia', 'Cambodia'),
        ('China', 'China'),
        ('India', 'India'),
        ('Japan', 'Japan'),
        ('Malaysia', 'Malaysia'),
        ('Turkey', 'Turkey'),
        ('Others', 'Others'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'country', 'required': 'required'})
    )

    class Meta:
        model = Register
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'image', 'place', 'country', 'password', 'confirm_password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields
        self.fields = {key: self.fields[key] for key in [
            'username', 'first_name', 'last_name', 'email', 'phone', 'image', 'place', 'country', 'password', 'confirm_password'
        ]}

    def clean_password(self):
        password = self.cleaned_data.get('password')
        PasswordChangeForm.validate_password(password)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("This field is required.")
        if Register.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_validator = RegexValidator(
            regex=r'^[6-9]\d{9}$',
            message="Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long."
        )
        try:
            phone_validator(phone)
        except ValidationError:
            raise forms.ValidationError("Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter again.")
        
        return cleaned_data



class DoctorRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    place = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'})
    )
    image = forms.ImageField(
        required=False,  # Making the image field optional
        label="Profile photo", # Updating the label to "Profile Photo"
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    SPECIALIZATION_CHOICES = [
        ('', 'Specialization*'),
        ('Cardiology', 'Cardiology'),
        ('Heart Surgery', 'Heart Surgery'),
        ('Skin Care', 'Skin Care'),
        ('Body Check-up', 'Body Check-up'),
        ('Numerology', 'Numerology'),
        ('Diagnosis', 'Diagnosis'),
        ('Others', 'Others'),
    ]
    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'department', 'required': 'required'})
    )
    

    
    COUNTRY_CHOICES = [
        ('', 'Country*'),
        ('Afghanistan', 'Afghanistan'),
        ('Armenia', 'Armenia'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Bhutan', 'Bhutan'),
        ('Cambodia', 'Cambodia'),
        ('China', 'China'),
        ('India', 'India'),
        ('Japan', 'Japan'),
        ('Malaysia', 'Malaysia'),
        ('Turkey', 'Turkey'),
        ('Others', 'Others'),
    ]

    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'country', 'required': 'required'})
    )
    
    # Customizing the order of fields in Meta class
    class Meta:
        model = Register
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 'image', 'place', 'country', 
            'qualification', 'specialization', 'experience', 'password', 'confirm_password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            
        }
        help_texts = {'username': None}

    def clean_qualification(self):
        qualification = self.cleaned_data.get("qualification")
        if not qualification.replace(" ", "").isalpha():
            self.add_error('qualification', "Qualification should contain only letters.")
        return qualification
    


    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if not any(char.isdigit() for char in experience):
            raise forms.ValidationError("Experience must include at least one numeric value (e.g., '5 years').")
        return experience

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter again.")
        
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        PasswordChangeForm.validate_password(password)
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_validator = RegexValidator(
            regex=r'^[6-9]\d{9}$',
            message="Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long."
        )
        try:
            phone_validator(phone)
        except ValidationError:
            raise forms.ValidationError("Invalid phone number. Please enter a valid 10-digit phone number starting with 6, 7, 8, or 9.")
        
        return phone

    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [ 'email', 'phone', 'place','image']
         
        widgets = {
            
            # "username" : forms.TextInput,
            # "email" : forms.EmailInput,
            # "phone" : forms.TextInput,
            # "place" : forms.TextInput
            
           }
        help_texts={
            "username":None
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_validator = RegexValidator(
            regex=r'^[6-9]\d{9}$',
            message="Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long."
        )
        try:
            phone_validator(phone)
        except ValidationError:
            raise forms.ValidationError("Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long.")
        return phone
    
    
class DRProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [ 'username','email', 'phone', 'place','image','specialization','qualification','experience']
         
        widgets = {
            
            "username" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            "specialization" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization'}),
            "qualification" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification'}),
            "experience" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience'}),
            "email" : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            "phone" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            "place" : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'}),
            
           }
        help_texts={
            "username":None
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_validator = RegexValidator(
            regex=r'^[6-9]\d{9}$',
            message="Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long."
        )
        try:
            phone_validator(phone)
        except ValidationError:
            raise forms.ValidationError("Phone number must start with 6, 7, 8, or 9 and must be exactly 10 digits long.")
        return phone

    

class LoginForm(forms.ModelForm):

    class Meta:
        model = Register
        fields = ['username', 'password']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            "password": forms.PasswordInput(attrs={"class": "form-control bg-transparent pswd", 'placeholder': 'Password'}),
        }
        help_texts = {'username': None}

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Validate the provided credentials
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password. Please try again.")
        else:
            if not username:
                self.add_error('username', "Username is required.")
            if not password:
                self.add_error('password', "Password is required.")
        
        return cleaned_data




class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,  # Set required to False to bypass required validation
        widget=forms.TextInput(attrs={'class': 'form-group'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Optionally, you can add custom cleaning logic here
        return cleaned_data

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )

    

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("The password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("The password must contain at least one letter.")
        
        # Add custom validation logic here
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        self.validate_password(new_password1)
        return new_password1
       
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        # Ensure the new password is different from the old password
        if old_password and new_password1 and old_password == new_password1:
            self.add_error('new_password1', "The new password must be different from the old password.")
        
        return cleaned_data
    
class SearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('symptoms', 'Symptoms'),
        ('ingredient', 'Ingredient'),
        ('disease', 'Disease'),
    ]
    
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    query = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search here...'}))





class RejectReasonForm(forms.ModelForm):

    class Meta:
        model = Register
        fields = ['reject_reason']
        
        widgets = {
           
             }
        