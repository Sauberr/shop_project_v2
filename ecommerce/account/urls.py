from django.contrib.auth import views as auth_views
from django.urls import path

from account.views import (dashboard, delete_account, email_verification,
                           email_verification_failed, email_verification_sent,
                           email_verification_success, my_login,
                           profile_management, register, user_logout, manage_shipping, check_email)

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('check-email/', check_email, name='check-email'),
    path('email-verification/<str:uid64>/<str:token>/', email_verification, name='email-verification'),
    path('email-verification-success/', email_verification_success, name='email-verification-success'),
    path('email-verification_failed/', email_verification_failed, name='email-verification-failed'),
    path('email-verification_sent/', email_verification_sent, name='email-verification-sent'),
    path('login/', my_login, name='my-login'),
    path('user-logout/', user_logout, name='user-logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile-management/', profile_management, name='profile-management'),
    path('delete-account/', delete_account, name='delete-account'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password/password-reset.html"), name='reset_password'),
    path('manage-shipping', manage_shipping, name='manage-shipping'),

]