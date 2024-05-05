from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa # type: ignore
from .models import Order, CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import SignupForm, LoginForm, Billing, BillingDetails,OrderForm
from .models import BillingDetails, Billing, Order
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

# SIGNUP
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            contact = form.cleaned_data['contact']
            address = form.cleaned_data['address']

            # Check if username is valid
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('signup')

            # Check if passwords match
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('signup')

            # Check password strength (you can implement your own logic here)
            if len(password1) < 8:
                messages.error(request, 'Password should be at least 8 characters long.')
                return redirect('signup')

            # Other validation checks can be added as needed

            user = form.save(commit=False)
            user.set_password(password1)
            user.save()
            send_confirmation_email(request, user)  # Send confirmation email
            messages.success(request, 'Please check your email to confirm your account.')
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = request.build_absolute_uri(reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token}))
    subject = 'Confirm your email address'
    message = f"Please click the following link to confirm your email address: {confirmation_link}"
    send_mail(subject, message, 'enote7y@gmail.com', [user.email])


# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_confirmed:
                    login(request, user)
                    return redirect('welcome')
                else:
                    form.add_error(None, 'Please confirm your email address to log in.')
            else:
                # Pass error message to the form
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})


# EMAIL CONFIRMATION
def confirm_email(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return render(request, 'email_confirmed.html')
    else:
        return render(request, 'email_confirmation_invalid.html')

def email_confirmation(request):
    return render(request, 'confirmation_email.html')

def email_confirmed(request):
    return render(request, 'email_confirmed.html')

def csrf_failure_view(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})

def email_confirmation_invalid(request):
    return render(request, 'email_confirmation_invalid.html')

# PASSWORD RESET
def send_password_reset_email(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist.')
        return None

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
    email_subject = 'Password Reset'
    email_body = render_to_string('password_reset_email.html', {'reset_url': reset_url})
    send_mail(email_subject, email_body, 'enote7y@gmail.com', [email])



def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcome')  # Redirect to welcome.html upon successful login
            else:
                form.add_error(None, 'Invalid email or password')  # Add error to form
                messages.error(request, 'Invalid email or password. Please try again.', extra_tags='danger')  # Display error message
                return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})





def logout(request):
    logout(request)
    return redirect('index')


from .forms import BillingDetailsForm

def welcome(request):
    if request.method == 'POST':
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = BillingDetailsForm()
    return render(request, 'welcome.html', {'form': form})

def success(request):
    return render(request, 'success.html')


def aboutUs(request):
    return render(request, 'aboutUs.html')

def coming_soon(request):
    return render(request, 'coming_soon.html')


from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def view_bills(request):
    billing_data = BillingDetails.objects.all()  # Fetch billing details from BillingDetails model
    context = {
        'billing_details': billing_data,
        'services_choices': dict(BillingDetails.SERVICES_CHOICES),  # Pass service choices to the template
    }
    return render(request, 'view_bills.html', context)



def paybill(request):
    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')

        if payment_option == 'pay_on_delivery':
            # Display a message or handle as needed for Pay On After Delivery option
            return render(request, 'pay_on_delivery_not_active.html')  # Render a template with the message

        # Redirect to the next page for other payment options
        return redirect('coming_soon')  # Replace 'next_page' with the actual URL name for the next page

    return render(request, 'paybill.html')


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_login')
def billing_details(request):
    if not request.user.is_staff:
        return redirect('index')
    billing_entries = Billing.objects.all()
    return render(request, 'billing_details.html', {'billing_details': billing_entries})

@staff_member_required(login_url='admin_login')
def review_orders(request):
    orders = Order.objects.all()
    return render(request, 'review_orders.html', {'orders': orders})



@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            service1 = form.cleaned_data['service1']
            service2 = form.cleaned_data['service2']
            service3 = form.cleaned_data['service3']

            # Create an Order object and save it to the database
            order = Order(service1=service1, service2=service2, service3=service3, customer=request.user)
            order.save()

            # Send confirmation email to the logged-in user
            user_email = request.user.email
            subject = f'Order Confirmation {request.user.username}'
            message = f'Dear {request.user.username},\n\nThank you for placing your order. You have selected the following services:\n\nService 1: {service1}\nService 2: {service2}\nService 3: {service3}\n\nTo confirm your order, please clear 20% of the payment. Visit our website for payment details here: http://127.0.0.1:8000/paybill/ .\n\nRegards,\nKasajja Cleaning Company'
            send_mail(subject, message, 'enote7y@gmail.com', [user_email])

            messages.success(request, 'Order placed successfully. Please check your email for order confirmation and payment details.')
            return redirect('success')  # Redirect to the success view
    else:
        form = OrderForm()

    return render(request, 'place_order.html', {'form': form})

 

from django.contrib.auth import authenticate, login

@user_passes_test(lambda u: u.is_superuser)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('billing_details')  # Redirect to 'billing_details' URL
        else:
            # Invalid credentials, handle the error as needed
            return render(request, 'index.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'index.html')


def pay_on_delivery_not_active(request):
        return render(request, 'pay_on_delivery_not_active.html')




@staff_member_required
def download_order_report(request):
    orders = Order.objects.all()
    users = CustomUser.objects.all()

    # Generate PDF content
    template_path = 'order_report_template.html'
    context = {'orders': orders, 'users': users}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF conversion error!', status=500)

    return response
