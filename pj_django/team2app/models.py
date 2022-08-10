from django.db import models

class Reviews(models.Model):
    writer = models.CharField(max_length=200)
    email = models.TextField(unique=True)
    subject = models.TextField()
    content = models.TextField()
    rdate = models.DateTimeField()
    views = models.TextField()
    
class Members(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(unique=True)
    pw = models.TextField()
    gender = models.CharField(max_length=200)
    addr = models.TextField()

class Review1(models.Model):
    writer = models.CharField(max_length=200)
    email = models.TextField()
    subject = models.TextField()
    content = models.TextField()
    rdate = models.DateTimeField()
    views = models.IntegerField()
    hosname = models.TextField()
    rating = models.IntegerField(null=True)    
    
class Member1(models.Model):
    name = models.CharField(max_length=200)
    email = models.TextField(unique=True)
    pw = models.TextField()
    gender = models.CharField(max_length=200)
    addr = models.TextField()
    phoneNum = models.TextField()
    
class Myevent(models.Model):
    email = models.TextField()
    title = models.TextField()
    hosname = models.TextField()