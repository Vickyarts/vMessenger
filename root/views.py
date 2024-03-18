from django.shortcuts import render
from django.http import HttpResponse
from usermanager.functions import *
from usermanager.models import ResetCode


# Create your views here.
def root(request):
    key = request.COOKIES.get('x-key')
    if validateUser(key):
        #return render(request, 'main-frame.html')
        response = HttpResponse('<html><script>window.location.replace("/x/");</script></html>')
        return response
    else: 
        try:
            if request.GET['redirect'] == '1':
                html = render(request,'login.html',{'option':{ 'account':False, 'credential':True }})
                return html
            elif request.GET['redirect'] == '2':
                html = render(request,'login.html',{'option':{ 'account':True, 'credential':False }})
                return html
            elif request.GET['redirect'] == '3':
                html = render(request,'login.html',{'option':{ 'account':False, 'credential':False, 'verified':True }})
                return html
            else:
                login_render = render(request, 'login.html')
                login_render.set_cookie('x-key', 'NONE')
                return login_render
        except:
            login_render = render(request, 'login.html')
            login_render.set_cookie('x-key', 'NONE')
            return login_render

def register(request):
    key = request.COOKIES.get('x-key')
    if validateUser(key):
        #return render(request, 'main-frame.html')
        response = HttpResponse('<html><script>window.location.replace("/x/");</script></html>')
        return response
    else: 
        return render(request, 'register.html')

def forgot(request):
    key = request.COOKIES.get('x-key')
    if validateUser(key):
        response = HttpResponse('<html><script>window.location.replace("/x/");</script></html>')
        return response
    else: 
        return render(request, 'forgot.html')

def reset(request):
    try:
        code = request.GET['c']
        if ResetCode.objects.filter(resetcode=code).exists():
            reset = ResetCode.objects.get(resetcode=code)
            return render(request, 'password.html', {'passcode':reset.passcode})
    except Exception as e:
        print(e)
        return HttpResponse('')


def mainFrame(request):
    key = request.COOKIES.get('x-key')
    if validateUser(key):
        return render(request, 'main-frame.html')
    else: 
        #return render(request, 'login.html')
        response = HttpResponse('<html><script>window.location.replace("/");</script></html>')
        return response
    
