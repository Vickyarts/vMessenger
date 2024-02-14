from django.urls import path
from .views import root, mainFrame, register


urlpatterns = [
    path('', root, name="ROOT"),
    path('register', register, name="RegisterPage"),
    path('x/', mainFrame, name="mainFrame")
]
