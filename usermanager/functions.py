from .models import User, models
import random
import string
import requests


def validateUser(token):
    try:
        x = User.objects.get(key=token)
        return True 
    except Exception as e:
        return False
    
def getUserId(token):
    try:
        x = User.objects.get(key=token)
        return x.id
    except:
        return None


def generateKey():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.sample(chars, k=18))

def generateVerifyCode():
    chars = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.sample(chars, k=12)) + ''.join(random.sample(chars, k=12))

def generateResetCode():
    chars = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.sample(chars, k=8)) + ''.join(random.sample(chars, k=8))

def generateUserId(model):
    max_serial = model.objects.aggregate(models.Max('id'))['id__max']
    print(max_serial)
    if max_serial is None:
        return 999999999999 + 1
    return max_serial + 1

def generateMessageId(model, message_type):
    max_serial = model.objects.aggregate(models.Max('id'))['id__max']
    if max_serial is None:
        if message_type == 'unseen':
            return 100000
        else:
            return 1000000
    return max_serial + 1


def sendEmail(name, subject, content):
    api_url = 'https://api.elasticemail.com/v2/email/send'
    api_key = 'D9E601E4609BF2D4ECCE49A260510FCC45E9EC18D40EAF477321DD1F2B9FC0500FC47FE45F9B8053859F6D4B08DFBEEC'
    params = {
        'apikey': api_key,
        'from': 'vmessenger@proton.me',
        'fromName': name,
        'to': 'vignesharplayboyvicky@gmail.com',
        'subject': subject,
        'bodyHtml': content,
        'isTransactional': True
    }
    response = requests.post(api_url, data=params)
    if response.status_code == 200:
        return True
    else:
        return False
