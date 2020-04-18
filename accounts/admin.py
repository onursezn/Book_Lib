from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from typing import Set

# Unregister the provided model admin
#admin.site.unregister(UserProfile)

# Register out own model admin, based on the default UserAdmin
@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):

    readonly_fields = [
        'password',
        'date_joined'
    ]
    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs): #Conditionally Prevent Update of Fields
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'email'
                'is_superuser',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form