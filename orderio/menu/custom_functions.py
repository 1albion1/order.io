from django.shortcuts import  render
from django.http.response import HttpResponse

def user_or_manager(request,path,context):
    if request.user.role.name == "manager":
        return render(request,f"menu/{path}.html",context)
    elif request.user.role.name == "user":
        return render(request,f"employee/{path}.html",context)
    else:
        return HttpResponse("User role not found!")