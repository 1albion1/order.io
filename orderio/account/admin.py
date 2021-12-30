from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Role
from main.forms import CreateUserForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CreateUserForm
    list_display = ('username','role','email','first_name','last_name')
    list_filter = ('role','is_superuser')
    fieldsets = (
        *UserAdmin.fieldsets,
        ( 
            "User Role", 
            {
                "fields":("role",)
                }
            )
        
    )
    
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Role)