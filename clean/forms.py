from django import forms
from .models import Billing, BillingDetails, CustomUser,Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    contact = forms.CharField(label='Contact', max_length=15, required=False)
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={'rows': 3}), required=False)
    confirmation_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'profile_picture', 'contact', 'address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

#USER MODEL
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


#password reset
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['services', 'date', 'time']


class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['services', 'date', 'time']

class OrderForm(forms.Form):
    SERVICE_CHOICES = [
        ('', 'Select a Service'),
        ('Basic House Cleaning', 'Basic House Cleaning'),
        ('Deep Cleaning', 'Deep Cleaning'),
        ('Spring Cleaning', 'Spring Cleaning'),
        ('Laundry Services', 'Laundry Services'),
    ]

    service1 = forms.ChoiceField(choices=SERVICE_CHOICES, label='Service 1')
    service2 = forms.ChoiceField(choices=SERVICE_CHOICES, label='Service 2', required=False)
    service3 = forms.ChoiceField(choices=SERVICE_CHOICES, label='Service 3', required=False)
