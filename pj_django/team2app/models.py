from django.db import models

class Review(models.Model):
    writer = models.CharField(max_length=200)
    email = models.TextField()
    subject = models.TextField()
    content = models.TextField()
    rdate = models.DateTimeField()
    views = models.IntegerField()
    hosname = models.TextField()
    rating = models.IntegerField(null=True)    
    
class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(unique=True)
    pw = models.TextField()
    gender = models.CharField(max_length=200)
    addr = models.TextField()
    phoneNum = models.TextField()

class Event(models.Model):
    hospital_name = models.CharField(max_length=200)
    event_name= models.TextField()
    rdate = models.DateTimeField()
    img_address = models.TextField()
    content = models.TextField()
    
class Myevent(models.Model):
    email = models.TextField()
    title = models.TextField()
    hosname = models.TextField()
    
class Book(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField()
    hosname = models.TextField()
    symptom = models.TextField()
    content = models.TextField()
    bdate = models.DateTimeField()
    btime = models.DateTimeField()
