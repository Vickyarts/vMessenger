from django.urls import path
from .views import root, mainFrame, register, forgot, reset, terms, policy


urlpatterns = [
    path('', root, name="ROOT"),
    path('register', register, name="RegisterPage"),
    path('forgot', forgot, name="ForgotPassword"),
    path('reset', reset, name="ResetPage"),
    path('x/', mainFrame, name="mainFrame"),
    path('terms', terms, name="Terms"),
    path('policy', policy, name="Policies"),
]