from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Message, UnseenMessage
from usermanager.models import User
from usermanager.functions import *
from datetime import date, time, datetime
import json



# Create your views here.
def getProfiles(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        try:
            #id = User.objects.get(key=xkey).id
            id = getUserId(xkey)
            msg_query = Message.objects.filter(Q(sender=id)|Q(receiver=id)).order_by('-id')
            unmsg_query = UnseenMessage.objects.filter(sender=id).order_by('-id')
            profile_addr = []
            profiles_added = []
            unprofile_addr = []
            unprofiles_added = []
            profiles = {}
            for message in msg_query:
                if message.receiver == id:
                    if not message.sender in profiles_added:
                        profile_addr.append({'id':message.sender, 'last':message.text, 'last_time':str(message.sent_time)})
                        profiles_added.append(message.sender)
                elif message.sender == id:
                    if not message.receiver in profiles_added:
                        profile_addr.append({'id':message.receiver, 'last':message.text, 'last_time':str(message.sent_time)})
                        profiles_added.append(message.receiver)
            for profile_data in profile_addr:
                try:
                    profile = User.objects.get(id=int(profile_data['id']))
                    profiles[str(profile.id)] = {'username':profile.username, 'display':profile.display, 'last':profile_data['last'], 'last_time':profile_data['last_time']}
                except Exception as e:
                    print(e)
            #UNSEEN
            for message in unmsg_query:
                if message.sender == id:
                    if not message.receiver in unprofiles_added:
                        unprofile_addr.append({'id':message.receiver, 'last':message.text, 'last_time':str(message.sent_time)})
                        unprofiles_added.append(message.receiver)
            for profile_data in unprofile_addr:
                try:
                    profile = User.objects.get(id=int(profile_data['id']))
                    profiles[str(profile.id)] = {'username':profile.username, 'display':profile.display, 'last':profile_data['last'], 'last_time':profile_data['last_time']}
                except Exception as e:
                    print(e)
            return HttpResponse(json.dumps(profiles))
        except Exception as e:
            return HttpResponse('{}')
    else:
        return HttpResponse('{}')


#def validateUser(x):
#    return True

def getMessages(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        try:
            id = User.objects.get(key=xkey).id
            #id = 1967853832591
            messaged, unseenmessaged = getMessaged(id)
            message_records = {}
            for user in messaged:
                messages = Message.objects.filter(Q(sender=user)&Q(receiver=id)|Q(sender=id)&Q(receiver=user)).order_by('-id')
                msg_stack = {}
                for msg in messages:
                    if msg.receiver == id:
                        msg_stack[str(msg.id)] = {'action':'received', 'text':msg.text, 'sent_time':str(msg.sent_time), 'sent_day':str(msg.sent_date)}
                    elif msg.sender == id:
                        msg_stack[str(msg.id)] = {'action':'sent', 'text':msg.text, 'sent_time':str(msg.sent_time), 'sent_day':str(msg.sent_date)}
                message_records[user] = msg_stack
            for user in unseenmessaged:
                unmessages = UnseenMessage.objects.filter(receiver=user).order_by('-id')
                msg_stack = {}
                for msg in unmessages:
                    if msg.sender == id:
                        msg_stack[str(msg.id)] = {'action':'sent', 'text':msg.text, 'sent_time':str(msg.sent_time), 'sent_day':str(msg.sent_date)}
                message_records[user] = msg_stack

            return HttpResponse(json.dumps(message_records))
        except Exception as e:
            return HttpResponse('{}')
    else:
        return HttpResponse('{}')
    
def getMessaged(id):
    texted = Message.objects.filter(Q(sender=id) | Q(receiver=id)).order_by('-id')
    unseentexted = UnseenMessage.objects.filter(sender=id).order_by('-id')
    messaged = []
    unmessaged = []
    for row in texted:
        if row.sender == id:
            if not row.receiver in messaged:
                messaged.append(row.receiver)
        elif row.receiver == id:
            if not row.sender in messaged:
                messaged.append(row.sender)
    for row in unseentexted:
        if not row.receiver in unmessaged:
            unmessaged.append(row.receiver)
    return messaged, unmessaged


def postMessage(request):
    xkey = request.POST['x-key']
    print(xkey)
    if validateUser(xkey):
        print('inside')
        message_id = generateMessageId(UnseenMessage, 'unseen')
        sender_id = getUserId(xkey)
        receiver_id = request.POST['id']
        message_text = request.POST['text']
        times = request.POST['time'].split(':')
        message_time = time(int(times[0]),int(times[1]),int(times[2]))
        days = request.POST['day'].split('-')
        message_day = date(int(days[0]),int(days[1]),int(days[2]))
        unseen = UnseenMessage(id=message_id, sender=sender_id, receiver=receiver_id,text=message_text,sent_date=message_day,sent_time=message_time)
        unseen.save()
        return HttpResponse(json.dumps({'exitcode':200}))
    else:
        return HttpResponse('{}')
    

def messageUpdates(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        updates = {}
        client_id = getUserId(xkey)
        unseen = UnseenMessage.objects.filter(receiver=client_id) #.order_by('-id')
        for msg in unseen:
            transfer_id = generateMessageId(Message, 'message')
            if msg.sender in updates:
                updates[msg.sender][transfer_id] = {'action':'received', 'text':msg.text, 'sent_time':str(msg.sent_time), 'sent_day':str(msg.sent_date)}
            else:
                updates[msg.sender] = {transfer_id: {'action':'received', 'text':msg.text, 'sent_time':str(msg.sent_time), 'sent_day':str(msg.sent_date)}}
            message_transfer = Message(id=transfer_id, sender=msg.sender, receiver=msg.receiver, text=msg.text, sent_date=msg.sent_date, sent_time=msg.sent_time)
            message_transfer.save()
            msg.delete()
        return HttpResponse(json.dumps(updates))
    else:
        return HttpResponse('{}')


def getProfilesByUsername(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        try:
            username = request.POST['username']
            client_id = getUserId(xkey)
            data = {}
            users = User.objects.filter(username__istartswith=username)
            if users.exists():
                for user in users:
                    if user.username != 'vMessenger' and user.id != client_id:
                        data[user.id] = { 'username':user.username, 'display':user.display, 'last_time':str(datetime.now().time()) }
            else:
                return HttpResponse('{}')
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse('{}')
    else:
        return HttpResponse('{}')
    
def getProfileById(request):
    xkey = request.POST['x-key']
    if validateUser(xkey):
        try:
            userid = request.POST['id']
            user = User.objects.get(id=userid)
            data = { 'id':user.id, 'display':user.display, 'username':user.username }
            print(data)
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse('{}')
    else:
        return HttpResponse('{}')






