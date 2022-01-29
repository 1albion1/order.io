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
        fields =( 'username','email','password1','password2','role','first_name','last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Confirm Password'})
        self.fields['role'].widget.attrs.update({'class': 'form-control','placeholder':'Role','required':True})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Last Name'})
       
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) <5:
            raise forms.ValidationError("Please enter a valid email.")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is already registered")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username already exists!")
        return username
    
class UserProfileForm(ModelForm):
    class Meta():
        model = Employee
        fields = '__all__'
        exclude = ['user','daily_allowance','wekly_allowance']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Username'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Phone Number'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Profile Picture'})
        
        
class FnameLnameForm(ModelForm):
    class Meta():
        model = CustomUser
        fields = ['first_name','last_name','email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Email'})      
        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user','placeholder':'Last Name'})
       
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) <5:
            raise ValidationError("Please enter a valid email.")
        return email