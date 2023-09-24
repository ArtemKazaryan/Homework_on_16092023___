from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('login/', views.loginuser, name='login'),
    path('singup/', views.signupuser, name='signup'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('profile/<pk>/', views.user_profile, name='user_profile')
]
