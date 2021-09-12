from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register, name='signup'),
    path('verification-email/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login, name='signin'),
    path('logout/', views.signout, name='logout'),
]