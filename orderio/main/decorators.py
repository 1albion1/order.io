from django.http import HttpResponse
from django.shortcuts import redirect

#checking if user is authenticated
def authenticated_user(view_func):
    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role.name == 'manager':
                return redirect("manager:index")
            elif request.user.role.name == 'user':
                return redirect("employee:index")
            else:
                return HttpResponse("The template for this user role is not ready yet.")
        return view_func(request,*args, **kwargs)
    return wrapper

#checking if user is in allowed roles
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            group = request.user.role.name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse(f"You are not authorised to view this page!")
        return wrapper
    return decorator