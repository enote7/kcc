from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('pay_on_delivery_not_active/', views.pay_on_delivery_not_active, name='pay_on_delivery_not_active'),
    path('signup/', views.signup, name='signup'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('welcome/', views.welcome, name='welcome'),
    path('paybill/', views.paybill, name='paybill'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('logout/', views.logout, name='logout'),
    path('success/', views.success, name='success'),
    path('view_bills/', views.view_bills, name='view_bills'),
    path('billing_details/', views.billing_details, name='billing_details'),  # This is the URL in question
    path('review_orders/', views.review_orders, name='review_orders'),
    path('place_order/', views.place_order, name='place_order'),
    path('confirm_email/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
    path('email_confirmation/', views.email_confirmation, name='email_confirmation'),
    path('email_confirmed/', views.email_confirmed, name='email_confirmed'),
    path('email_confirmation_invalid/', views.email_confirmation_invalid, name='email_confirmation_invalid'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    path('download_order_report/', views.download_order_report, name='download_order_report'),
]
