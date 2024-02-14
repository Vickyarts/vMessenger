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