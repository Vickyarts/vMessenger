from django.urls import path
from .views import *


urlpatterns = [
    path('profileimage', profileImages, name="ProfileImages"),
]
