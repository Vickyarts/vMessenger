from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Verify, ResetCode
from datahub.models import Message, UnseenMessage
from .functions import *
from datetime import date, datetime
import json


HOST = '127.0.0.1'
PORT = '8000'

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
            reg = User(id=userid, key='UgbBYNCjNrpdSSPvBJ', email=email, username=username, display=display, dob = dob, joined_at=date.today(), password = password)
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
    url = f'http://{HOST}:{PORT}/users/verify?c={code}'
    content = f'<p style="font-family:Arial;font-size:14px;"> An vMessenger account has create on this e-mail.<br><br> <b>Please verify this email belongs to you.</b><br><br> <a href="{url}" style="color:378CE7;" target="_blank">Verify email</a><br><br> Verification ensures we can safely assist you in case of sign-in issues or suspicious activity.<br><br> Thank you,<br> vMessenger Team<br> <p>'
    sendEmail("vMessenger", "Email Verification", email, content)
    pact.save()

def initiate_ProjectIntro(id,name):
    current_date = date.today()
    current_time = datetime.now().time()
    x1_id = generateMessageId(UnseenMessage, 'unseen')  #generateMessageId(Message, 'message')
    x1 = UnseenMessage(id=x1_id, sender=999999999999,receiver=id,text='Hi '+name+'!', sent_date=current_date, sent_time=current_time)
    x1.save()
    x2_id = generateMessageId(UnseenMessage, 'unseen')  #generateMessageId(Message, 'message')
    x2 = UnseenMessage(id=x2_id, sender=999999999999,receiver=id,text='Welcome to vMessenger!', sent_date=current_date, sent_time=current_time)
    x2.save()
    x3_id = generateMessageId(UnseenMessage, 'unseen')  #generateMessageId(Message, 'message')
    x3 = UnseenMessage(id=x3_id, sender=999999999999,receiver=id,text=" Feel free to explore and discover all its features. If you have any questions or need assistance, don't hesitate to <a href='mailto:vigneshar24@protonmail.com'>reach out</a>. Enjoy exploring!", sent_date=current_date, sent_time=current_time)
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

def forgot(request):
    mail = request.POST['email']
    try:
        user = User.objects.get(email=mail)
        resetcode = generateResetCode()
        passcode = generateVerifyCode()
        try:
            reset = ResetCode.objects.get(email=mail)
            reset.delete()
            code = ResetCode(userid=user.id, email=mail, resetcode=resetcode, passcode=passcode)
            code.save()
            url = f'http://{HOST}:{PORT}/reset?c={resetcode}'
            content = f'<p style="font-family:Arial;font-size:14px;"> Password reset has been initiated on this account.<br><br> <b>Click below to reset you password.</b><br><br> <a href="{url}" style="color:378CE7;" target="_blank">Reset</a><br><br>Make sure your password is strong to ensure security.<br><br> Thank you,<br> vMessenger Team<br> <p>'
            sendEmail("vMessenger", "Password Reset", mail, content)
        except:
            code = ResetCode(userid=user.id, email=mail, resetcode=resetcode, passcode=passcode)
            code.save()
            url = f'http://{HOST}:{PORT}/reset?c={resetcode}'
            content = f'<p style="font-family:Arial;font-size:14px;"> Password reset has been initiated on this account.<br><br> <b>Click below to reset you password.</b><br><br> <a href="{url}" style="color:378CE7;" target="_blank">Reset</a><br><br>Make sure your password is strong to ensure security.<br><br> Thank you,<br> vMessenger Team<br> <p>'
            sendEmail("vMessenger", "Password Reset", mail, content)
            return HttpResponse('{}')
    except Exception as e:
        print(e)
        return HttpResponse('{}')

def passreset(request):
    passcode = request.POST['passcode']
    password = request.POST['pass']
    try:
        reset = ResetCode.objects.get(passcode=passcode)
        user = User.objects.get(id=reset.userid)
        user.password = password
        user.save()
        reset.delete()
        return HttpResponse('200')
    except Exception as e:
        print(e)
        return HttpResponse('404')


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
    return render(request, 'password.html')