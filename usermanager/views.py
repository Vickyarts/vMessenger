from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import User, Verify
from datahub.models import Message
from .functions import *
from datetime import date, datetime
import json


# Create your views here.
def login(request):
    mail = request.POST['email']
    passw = request.POST['pass']
    try:
        x = User.objects.get(email=mail)
        if x.password == passw:
            if x.verified:
                x.key = generateKey()
                x.save()
                response = HttpResponse('<html><script>window.location.replace("/x/");</script></html>')
                response.set_cookie('x-key', x.key, max_age=864000)
                return response
            else:
                html = HttpResponse('<html><script>window.location.replace("/?redirect=3");</script></html>')
                return html
        else:
            html = HttpResponse('<html><script>window.location.replace("/?redirect=1");</script></html>')
            return html
    except Exception as e:
        print(e)
        html = HttpResponse('<html><script>window.location.replace("/?redirect=2");</script></html>')
        return html

def logout(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        id = getUserId(xkey)
        user = User.objects.get(id=id)
        user.key = generateKey()
        user.save()
        return HttpResponse(json.dumps({'logout':200}))
    else:
        return HttpResponse(json.dumps({'logout':404}))

def register(request):
    try:
        email = request.POST['email']
        display = request.POST['display']
        username = request.POST['username'].lower()
        if not User.objects.filter(Q(email=email)|Q(username=username)).exists():
            userid = generateUserId(User)
            dob = date(int(request.POST['year']), int(request.POST['month']), int(request.POST['day']))
            password = request.POST['pass']
            reg = User(id=userid, key='nil', email=email, username=username, display=display, dob = dob, joined_at=date.today(), password = password)
            initiate_UserVerification(userid, email)
            initiate_ProjectIntro(userid,display)
            reg.save()
            return render(request, 'verify.html')
        else:
            html = HttpResponse('<html><script>window.location.replace("/register");</script></html>')
            return html
    except Exception as e:
        print(e)
        html = HttpResponse('<html><script>window.location.replace("/");</script></html>')
        return html
    

def initiate_UserVerification(userid, email):
    code = generateVerifyCode()
    pact =  Verify(userid=userid, email=email, code=code)
    pact.save()

def initiate_ProjectIntro(id,name):
    current_date = date.today()
    current_time = datetime.now().time()
    x1_id = generateMessageId(Message, 'message')
    x1 = Message(id=x1_id, sender=999999999999,receiver=id,text='Hi '+name+'!', sent_date=current_date, sent_time=current_time)
    x1.save()
    x2_id = generateMessageId(Message, 'message')
    x2 = Message(id=x2_id, sender=999999999999,receiver=id,text='Welcome to vMessenger!', sent_date=current_date, sent_time=current_time)
    x2.save()
    x3_id = generateMessageId(Message, 'message')
    x3 = Message(id=x3_id, sender=999999999999,receiver=id,text=" Feel free to explore and discover all its features. If you have any questions or need assistance, don't hesitate to <a href='mailto:vigneshar24@protonmail.com'>reach out</a>. Enjoy exploring!", sent_date=current_date, sent_time=current_time)
    x3.save()


def verify(request):
    try:
        code = request.GET['c']
        verify_email = Verify.objects.get(code = code)
        user = User.objects.get(id=verify_email.userid)
        user.verified = True
        user.save()
        verify_email.delete()
        return render(request, 'verified.html')
    except:
        return render(request, 'notfound.html')

def usernameAvailable(request):
    try:
        username = request.POST['username']
        data = {'username':200}
        if username != '':
            try:
                user = User.objects.get(username=username)
                data['username'] = 404
            except:
                data['username'] = 200
        return HttpResponse(json.dumps(data))
    except:
        data = {'username':200}
        return HttpResponse(json.dumps(data))
    

def test(request):
    username = request.GET['p']
    if not User.objects.filter(Q(username=username)).exists():
        return HttpResponse('Username is available')
    else:
        return HttpResponse('Username already used')