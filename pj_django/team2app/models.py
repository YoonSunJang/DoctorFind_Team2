from django.db import models

class Review(models.Model):
    subject = models.CharField(max_length=200)
    users = models.TextField()
    rdate = models.DateTimeField()
    inquiry = models.TextField()
    content = models.TextField()
    
class Event(models.Model):
    hospital_name = models.CharField(max_length=200)
    event_name= models.TextField()
    rdate = models.DateTimeField()
    img_address = models.TextField()
    content = models.TextField()