from django.contrib import admin

from employee.models import Department, Employee

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)