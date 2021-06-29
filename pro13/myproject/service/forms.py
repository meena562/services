from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from service.models import User,CarCategory,Services,Customise,RoleRqst, Myorders

from django.contrib.auth import get_user_model

User = get_user_model()
class UsForm(UserCreationForm):
	password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border-success","placeholder":"enter password"}))
	password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border-success","placeholder":"confirm password"}))


	class Meta:
		model=User
		fields = ['username','email']
		widgets = {
		"username":forms.TextInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter Username",
			"required":True,
			}),
		"email":forms.EmailInput(attrs = {
			"class":"form-control",
			"placeholder":"Enter emailid",
			"required":True,
			}),
		}
class RoleR(forms.ModelForm):
	class Meta:
		model = RoleRqst
		fields= ["uname","roletype","proof"]
		widgets={
		"uname":forms.TextInput(attrs={"class":"form-control my-2","readonly":True}),
		"roletype":forms.Select(attrs = {"class": "form-control my-2",}),
		"proof":forms.ClearableFileInput(attrs={"class":"form-control"}),

		}
class RoleUp(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","role"]
		widgets={
		"username": forms.TextInput(attrs={"class":"form-control","readonly":True,}),
		"role":forms.Select(attrs={"class":"form-control"}),
		}

		
class UpdPfle(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","email","first_name","last_name","city","state","pin","address","age"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control",
			"readonly":True,
			}),
		"first_name":forms.TextInput(attrs={"class":"form-control","placeholder":"update first_name","required":True,}),
		"last_name":forms.TextInput(attrs={"class":"form-control","placeholder":"update last_name","required":True,}),
		"email":forms.EmailInput(attrs={"class":"form-control","placeholder":"update email","required":True,}),
		"age":forms.NumberInput(attrs={"class":"form-control","placeholder":"update age","required":True,}),
		"car_regno":forms.TextInput(attrs={"class":"form-control","placeholder":"update car_regno","required":True,}),
		"address":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"address"}),
		"email":forms.EmailInput(attrs={"class":"form-control my-2","placeholder":"Enter your email"}),
		"phno":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"Phone number"}),
		"city":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"city"}),
		"state":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"state"}),
		"pin":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"Pincode"}),
		}
		
		
class Userupdate(forms.ModelForm):
	class Meta:
		model=Services
		fields=["service_type","sid","price"]
		widgets = {
		"service_type":forms.TextInput(attrs= {
			"class":"form-control","placeholder":"select car_make",
			}),
		"sid":forms.TextInput(attrs= {
			"class":"form-control","placeholder":"select car_make",
			}),
		"price":forms.NumberInput(attrs={
			"class":"form-control",
			"placeholder":"Enter Price",
			}),
		}
class CancelForm(forms.ModelForm):
	class Meta:
		model=Myorders
		fields=["service_type","price","cancel",]
		widgets={
		"pname":forms.TextInput(attrs={"class":"form-control"}),
		"price":forms.TextInput(attrs={"class":"form-control"}),
		"cancel":forms.Select(attrs={"class":"form-control"})
		}

class ChpwdForm(PasswordChangeForm):
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Old Password"}))
	new_password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"New Password"}))
	new_password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}))
		
	class Meta:
		model=['oldpassword','newpassword','confirmpassword']
class ImForm(forms.ModelForm):
	class Meta:
		model=User
		fields=["first_name","last_name","age","gender","impf","phno","car_regno","address",]
		widgets={
		"first_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter First name"}),
		"last_name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Last name"}),
		"age":forms.NumberInput(attrs={"class":"form-control","placeholder":"Update your age"}),
 		"gender":forms.Select(attrs={"class":"form-control","placeholder":"select your gender"}),
		"phno":forms.NumberInput(attrs={"class":"form-control","placeholder":"Enter phone number"}),
		"car_regno":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter carreg number"}),
		"address":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter address"}),
		}

class CategoryForm(forms.ModelForm):
	class Meta:
		model=CarCategory
		fields=["cname"]
		widgets={
		"cname":forms.TextInput(attrs={"class":"form-control","placeholder":"enter cname"}),
		}
class AddForm(forms.ModelForm):
	class Meta:
		model=Services
		fields=["service_type","price","sid","is_status"]
		widgets = {
		"service_type":forms.TextInput(attrs= {
			"class":"form-control","placeholder":"Enter service_type",
			}),
		"price":forms.NumberInput(attrs= {
			"class":"form-control","placeholder":"enter price",
			}),
		}
class CustomiseForm(forms.ModelForm):
	class Meta:
		model=Customise
		fields=["uname","email","phno","carcategory","description"]
		widgets={
		"uname":forms.TextInput(attrs=
			{
			"class":"form-control",
			"placeholder":"Enter your name"
			}),
		"phno":forms.NumberInput(attrs={"class":"form-control"}),
		"email":forms.EmailInput(attrs={"class":"form-control","placeholder":"enter email"}),
		"carcategory":forms.Select(attrs={"class":"form-control"}),
		
		}
class Shipform(forms.ModelForm):
	class Meta:
		model=User
		fields=["phno","address","city","state","pin"]
		widgets = {
		"phno":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"Phone number"}),
		"city":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"city"}),
		"address":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"address"}),
		"state":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"state"}),
		"pin":forms.TextInput(attrs={"class":"form-control my-2","placeholder":"Pincode"}),
		"date":forms.DateInput(attrs={"class":"form-control my-2","placeholder":"date"}),
		}

