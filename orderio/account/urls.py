from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login",views.login_page,name="login"),
    path("register",views.register,name="register"),
    path("logout",views.logout_user,name="logout"),
    path("create_user",views.create_user,name="create_user"),
    path("user_list",views.user_list,name="user_list"),
    path("delete_user/<int:pk>",views.delete_user,name="delete_user"),
    #path("update_user/<int:pk>",views.update_user,name="update_user"),
    #password
    path("reset_password/",auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),name="reset_password"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"),name="password_reset_confirm"),
    path("reset_password_complete",auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"),name="password_reset_complete"),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='account/change_password.html',success_url = '/'),
         name='change_password'),
]
