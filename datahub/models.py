from django.db import models


# Create your models here.
class Message(models.Model):
    sender = models.BigIntegerField()
    receiver = models.BigIntegerField()
    text = models.TextField()
    sent_date = models.DateField()
    sent_time = models.TimeField()

class UnseenMessage(models.Model):
    sender = models.BigIntegerField()
    receiver = models.BigIntegerField()
    text = models.TextField()
    sent_date = models.DateField()
    sent_time = models.TimeField()
