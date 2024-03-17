from django.urls import path 
from .views import *


urlpatterns = [
    path('login', login, name="Login"),
    path('logout', logout, name="Logout"),
    path('register', register, name="Register"),
    path('verify', verify, name="EmailVerify"),
    path('forgot', forgot, name="ForgotPass"),
    path('passwordreset', passreset, name="PassReset"),
    path('usernamecheck', usernameAvailable, name="Username Check"),
    path('test', test, name="Test"),
]
