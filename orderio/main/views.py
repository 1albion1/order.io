from django.shortcuts import render
from main.decorators import authenticated_user
# Create your views here.
@authenticated_user
def index(request):
    return render(request,'main/index.html')