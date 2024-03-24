from django.urls import path
from .views import *


urlpatterns = [
    path('messages', getMessages, name="GetAllMessages"),
    path('profiles', getProfiles, name="GetProfiles"),
    path('postmessage', postMessage, name="PostMessage"),
    path('messageupdates', messageUpdates, name="MessageUpdates"),
    path('usernamesearch', getProfilesByUsername, name="GetProfileByUsername"),
    path('userid', getProfileById, name="GetProfileById")
]
