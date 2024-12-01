from django.shortcuts import render
from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserProfileView, logout, UserCartView

app_name = 'account'

urlpatterns = [
    path('users-cart/', UserCartView.as_view(), name='users_cart'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),

    #Registration and verification

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('email-verification-sent/',
     lambda request: render(request, 'accounts/email/email-verification-sent.html'), 
     name='email_verification_sent'),

#     #Login & Logout
#     path('login/', views.login_user, name='login'),
#     path('logout/', views.logout_user, name='logout'),

#     #Dashboard
#     path('dashboard/', views.dashboard_user, name='dashboard'),
#     path('profile-management/', views.profile_user, name='profile-management'),
#     path('delete-user/', views.delete_user, name='delete-user'),
]