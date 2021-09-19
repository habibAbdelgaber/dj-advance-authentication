from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.signout, name='logout'),
    path('signup/', views.register, name='signup'),
    path('verification-email/<uidb64>/<token>/', views.activate, name='activate'),

    # Password Reset
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/done/<uidb64>/<token>/', views.password_reset_done, name='password_reset_done'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]