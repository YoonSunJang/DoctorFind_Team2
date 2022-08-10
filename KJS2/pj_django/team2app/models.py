from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=30)
    email = models.TextField(primary_key=True)
    phone = models.TextField(max_length=30)
    pw = models.TextField(max_length=30)
    address = models.TextField()