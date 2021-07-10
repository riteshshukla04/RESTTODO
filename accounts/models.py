from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=200)
    

