from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import CustomUser, Billing, BillingDetails, Order

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_superuser')  
    search_fields = ('email', 'username')
    readonly_fields = ('last_login',)  

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('contact', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'profile_picture', 'contact', 'address')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(BillingDetails)
