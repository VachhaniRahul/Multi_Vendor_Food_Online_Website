from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role',)
    ordering = ('-date_joined',)
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'role', 'password1', 
                'password2','is_admin', 'is_staff', 'is_active', 'is_superadmin'
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)