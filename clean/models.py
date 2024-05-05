from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, contact=None, address=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, contact=contact, address=address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, contact=None, address=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, contact, address, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    contact = models.CharField(_('contact'), max_length=15, blank=True, null=True)
    address = models.TextField(_('address'), blank=True, null=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pics/', blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

from django.contrib.auth import get_user_model

class Billing(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    services = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Billing for {self.customer.email}"



class BillingDetails(models.Model):
    SERVICES_CHOICES = [
        ('Basic House Cleaning', 'Basic House Cleaning'),
        ('Deep Cleaning', 'Deep Cleaning'),
        ('Spring Cleaning', 'Spring Cleaning'),
        ('Laundry Services', 'Laundry Services'),
    ]

    services = models.CharField(max_length=20, choices=SERVICES_CHOICES)
    date = models.DateField()
    time = models.TimeField()


class Order(models.Model):
    SERVICE_CHOICES = [
        ('Basic House Cleaning', 'Basic House Cleaning'),
        ('Deep Cleaning', 'Deep Cleaning'),
        ('Spring Cleaning', 'Spring Cleaning'),
        ('Laundry Services', 'Laundry Services'),
    ]

    service1 = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    service2 = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=True)
    service3 = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        services = [self.service1]
        if self.service2:
            services.append(self.service2)
        if self.service3:
            services.append(self.service3)
        return ', '.join(services)