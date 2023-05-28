from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.forms.fields import ImageField
from datetime import datetime, timedelta
# Create your models here.

def mydate():
    return datetime.now() + timedelta(days=1)

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    images = models.ImageField(upload_to='Upload Media Root')
    first_name = models.CharField(max_length=30, default=mydate)
    last_name = models.CharField(max_length=30, default=mydate)
    Bio = models.CharField(max_length=300)

    def __str__(self):
        return str(self.user)

class User(models.Model):
    user = models.CharField(default=None, max_length=20)
    def __str__(self):
        return self.user
