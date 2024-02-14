from django.urls import path 
from .views import *


urlpatterns = [
    path('login', login, name="Login"),
    path('logout', logout, name="Logout"),
    path('register', register, name="Register"),
    path('verify', verify, name="EmailVerify"),
    path('usernamecheck', usernameAvailable, name="Username Check"),
    path('test', test, name="Test"),
]
