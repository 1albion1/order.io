from django.contrib.auth.forms import  UserCreationForm
from django import forms
from account.models import CustomUser
from django.forms import ModelForm
from employee.models import Employee
from django.core.exceptions import ValidationError

class EmployeeForm(ModelForm):
    class Meta():
        model = Employee
        fields = '__all__'
        exclude = ['user','weekly_allowance']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =( 'username','email','password1','password2','role')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username already exists!")
        return username
    
class UserProfileForm(ModelForm):
    class Meta():
        model = Employee
        fields = '__all__'
        exclude = ['user','daily_allowance','wekly_allowance']

        
    