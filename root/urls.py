from django.urls import path
from .views import root, mainFrame, register, forgot, reset


urlpatterns = [
    path('', root, name="ROOT"),
    path('register', register, name="RegisterPage"),
    path('forgot', forgot, name="ForgotPassword"),
    path('reset', reset, name="ResetPage"),
    path('x/', mainFrame, name="mainFrame")
]
