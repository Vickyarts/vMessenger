from django.shortcuts import render
from django.http import FileResponse
import os


# Create your views here.
def profileImages(request):
    try:
        id = request.GET['id']
        image_path = f'assetmanager/files/profile-images/{id}.png'
        if os.path.exists(image_path):
            return FileResponse(open(image_path,'rb'))
        elif id == 'va':
            return FileResponse(open('assetmanager/files/profile-images/va.png','rb'))
        else:
            return FileResponse(open('assetmanager/files/profile-images/default.png','rb'))
    except:
        return FileResponse(open('assetmanager/files/profile-images/default.png','rb'))