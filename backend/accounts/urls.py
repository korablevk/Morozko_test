from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy
from .views import UserLoginView, UserRegistrationView, UserProfileView, logout, UserCartView

app_name = 'account'

urlpatterns = [
    path('users-cart/', UserCartView.as_view(), name='users_cart'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('email-verification-sent/',
     lambda request: render(request, 'accounts/email/email-verification-sent.html'), 
     name='email_verification_sent'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password/password-reset.html',
        email_template_name='accounts/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password/password-reset-done.html'),
        name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password/password-reset-confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password/password-reset-complete.html'),
        name='password_reset_complete'),
]