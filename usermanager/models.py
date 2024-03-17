from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    key = models.CharField(max_length=18)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    display = models.CharField(max_length=50)
    dob = models.DateField()
    joined_at = models.DateField()
    password = models.CharField(max_length=48)
    verified = models.BooleanField(default=False)

class Verify(models.Model):
    userid = models.BigIntegerField()
    email = models.CharField()
    code = models.CharField()

class ResetCode(models.Model):
    userid = models.BigIntegerField()
    email = models.CharField()
    resetcode = models.CharField()
    passcode = models.CharField()