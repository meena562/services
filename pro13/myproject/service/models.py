from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
	t = (
		(1,'owner'),
		(2,'customer'),
		(3,'Anonymous'),
		)
	role = models.IntegerField(default=3,choices=t)
	g=[('M',"Male"),('F','Female')]
	age=models.IntegerField(default=10)
	impf=models.ImageField(upload_to='Profiles/',default="Note.jpg")
	gender=models.CharField(max_length=10,choices=g)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	car_regno=models.CharField(max_length=20)
	phno=models.CharField(null='True',max_length=30)
	address=models.TextField(null='True')
	city=models.CharField(max_length=30,null='True')
	state=models.CharField(max_length=40,null='True')
	pin=models.IntegerField(null='True')
	nameoncard=models.CharField(max_length=30,null='True')
	creditcardnumber=models.IntegerField(null='True')
	Expyear=models.DateField(null='True')
	expmonth=models.CharField(max_length=20,null='True')
	cvv=models.IntegerField(null='True')
	date=models.DateField(null='True')
class RoleRqst(models.Model):
	t=[(1,'owner'),(2,'customer')]
	uname= models.CharField(max_length=30)
	roletype = models.PositiveIntegerField(choices=t)
	proof = models.ImageField(null=True)
	is_checked=models.BooleanField(default=0)
	uid= models.OneToOneField(User,on_delete=models.CASCADE)
# # class ImProfile(models.Model):
# 	g = [('M',"Male"),('F','Female')]
# 	first_name=models.CharField(max_length=100)
# 	last_name=models.CharField(max_length=100)
# 	email=models.EmailField(max_length=100)
# 	phone_no=models.IntegerField(max_length=10)
# 	car_regno=models.TextField(max_length=8)
# 	age = models.IntegerField(default=10)
# 	impf = models.ImageField(upload_to='Profiles/',default="profile.png")
# 	gender = models.CharField(max_length=10,choices=g)
class CarCategory(models.Model):
	cname=models.CharField(max_length=20)
	def __str__(self):
		return self.cname
class Services(models.Model):
	service_type=models.CharField(max_length=30)
	price=models.IntegerField()
	sid=models.ForeignKey(CarCategory,on_delete=models.CASCADE)
	is_status=models.IntegerField(default=1)
	def __str__(self):
		return self.sname

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	service=models.ForeignKey(Services,on_delete=models.CASCADE)


class Myorders(models.Model):
	service_type=models.CharField(max_length=30)
	price=models.IntegerField()
	a=[("I don't want this service_type","I don't want this service_type"),("I want to change address/phone number","I want to change address/phone number"),("High cost of service","High cost of service"),("others","others")]
	cancel=models.CharField(max_length=200,choices=a,null=True)
	is_status=models.IntegerField(default=1)
	date=models.DateTimeField(auto_now_add='True',null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
class Customise(models.Model):
	uname=models.CharField(max_length=10)
	email=models.EmailField()
	phno=models.IntegerField()
	a=[('Audi',"Audi"),('Toyota',"Toyota"),('Shift',"Shift"),('pollo',"pollo")]
	carcategory=models.CharField(max_length=20,choices=a)
	description=models.TextField(max_length=500)
class shipping(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)





