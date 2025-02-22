from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User

    # Fields to display in the list view
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender')

    # Fields to search in the admin panel
    search_fields = ('email', 'first_name', 'last_name')

    # Correct ordering
    ordering = ('email',)  # 'username' ni olib tashladik, chunki u yo‘q

    # Define fieldsets for editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'birth_date', 'gender')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login',)}),
    )

    # Define fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )

    # Enable editing of password from the admin panel
    change_password_form = BaseUserAdmin.change_password_form


# Register the models with the custom admin classes
admin.site.register(User, UserAdmin)
