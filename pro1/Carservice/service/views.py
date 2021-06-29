from django.shortcuts import render,redirect
from service.forms import UsForm,ServiceForm,Userupdate,ChpwdForm,UpdPfle,CategoryForm,AddForm
from django.core.mail import send_mail
from carservice import settings
from django.contrib import messages
from service.models import UserService
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from service.models import User,CarCategory,Services
# Create your views here
def home(request):
	cf=CarCategory.objects.all()
	return render(request,'services/home.html',{'data':cf})

def about(request):
	cf=CarCategory.objects.all()
	return render(request,'services/about.html',{'data':cf})

def contact(request):
	cf=CarCategory.objects.all()
	return render(request,'services/contact.html',{'data':cf})
def booking(request):
	cf=CarCategory.objects.all()
	return render(request,'services/booking.html',{'data':cf})
def cart(request):
	return render(request,'/services/cart.html')

def viewuser(request):
	p=User.objects.all()
	return render(request,'services/viewuser.html',{'u':p})

def customer(request,id):
	a=User.objects.get(id=id)
	a.role="2"
	a.save()
	return redirect('/viewuser',)

def owner(request,id):
	a=User.objects.get(id=id)
	a.role="1"
	a.save()
	return redirect('/viewuser')

def registration(request):
	cf=CarCategory.objects.all()
	if request.method=="POST":
		p=UsForm(request.POST)
		if p.is_valid():
			p.save()
			return redirect('/log')
			
	p=UsForm()
	return render(request,'services/register.html',{'u':p},{'s':cf})

def Service(request):
	if request.method=="POST":
		j=ServiceForm(request.POST,request.FILES)
		if j.is_valid():
			i=j.save(commit=False)
			i.uid_id=request.user.id
			i.save()
			return redirect('/showdata')
	j=ServiceForm()
	return render(request,'services/Services.html',{'u':j})
def role(request):
	return render(request,'services/role.html')

def deletedata(req,st):
	data=UserService.objects.get(id=st)
	data.delete()
	return redirect('/cr')
def addcategory(request):
	if request.method=="POST":
		a=CategoryForm(request.POST)
		if a.is_valid():
			a.save()
			return redirect('/home')
	cf=CategoryForm()
	return render(request,'services/addcategory.html',{'c':cf})
def addcarservices(request):
	if request.method=="POST":
		b=AddForm(request.POST)
		if b.is_valid():
			b.save()
			return redirect('/home')
	se=AddForm()
	return render(request,'services/addcarservices.html',{'e':se})

def showinfo(req):
	cf=CarCategory.objects.all()
	data=UserService.objects.all()
	return render(req,'services/showdata.html',{'info':data},{'u':cf})

def infodelete(req,et):
	data=UserService.objects.get(id=et)
	if req.method == "POST":
		data.delete()
		return redirect('/showdata')
	return render(req,'services/userdelete.html',{'sd':data})

def userupdate(up,si):
	t=UserService.objects.get(id=si)
	if up.method=="POST":
		d=Userupdate(up.POST,instance=t)
		if d.is_valid():
			d.save()
			return redirect('/showdata')
	d=Userupdate(instance=t)
	return render(up,'services/updateuser.html',{'us':d})

def carddetails(request):
	return render(request,'services/carddetails.html')





def profile(req):
	return render(req,'services/profile.html')
def dashboard(req):
	return render(req,'services/dashboard.html')

def cgf(re):
	if re.method=="POST":
		c=ChpwdForm(user=re.user,data=re.POST)
		if c.is_valid():
			c.save()
			return redirect('/log')
	c=ChpwdForm(user=request)
	return render(re,'services/changepassword.html',{'t':c})	

def updprofile(request):
	if request.method == "POST":
		t = UpdPfle(request.POST,instance=request.user)
		if t.is_valid():
			t.save()
			return redirect('/pro')
	t = UpdPfle(instance=request.user)
	return render(request,'services/updateprofile.html',{'z':t})	
def categories(request,id):
	d=CarCategory.objects.all()
	p=services.objects.filter(sid_id=id)
	return render(request,'services/carservices.html',{'da':p,'data':d})												
