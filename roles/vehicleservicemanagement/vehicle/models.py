from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	r=[(1,'owner'),(2,'customer'),(3,'guest')]
	age=models.IntegerField(null=True)
	phonenum=models.CharField(max_length=10,null=True)
	rl=models.CharField(max_length=10,choices=r,default=3)