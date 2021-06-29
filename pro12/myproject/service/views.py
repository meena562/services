from django.shortcuts import render,redirect
from service.forms import UsForm,Userupdate,ChpwdForm,UpdPfle,CategoryForm,AddForm,CustomiseForm,RoleR,RoleUp
from django.core.mail import send_mail
from carservice import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from service.models import User,CarCategory,Services,Cart,Myorders,Customise,RoleRqst
from django.core.mail import send_mail,EmailMessage
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here
def home(request):
	cf=CarCategory.objects.all()
	return render(request,'services/home.html',{'data':cf})

def about(request):
	cf=CarCategory.objects.all()
	return render(request,'services/about.html',{'data':cf})
def dash(request):
	return render(request,'services/dashboard.html')
def contact(request):
	cf=CarCategory.objects.all()
	return render(request,'services/contact.html',{'data':cf})
def rolereq(request):
	if request.method== "POST":
		k =RoleR(request.POST,request.FILES)
		if k.is_valid():
			s=k.save(commit=False)
			s.uname= request.user.username
			s.uid_id= request.user.id
			s.save()
			message='service type ::\n'+' ,'.join(l1)+'\n'+ ' will be contact you.\n'+'Total amount paid: Rs.'+str(sum)+'\n'+'THANK YOU for request!!'
			subject='service booked'
			sender=settings.EMAIL_HOST_USER
			t=EmailMessage(subject,message,sender)
			t.send()
			return redirect('/dash')
	k=RoleR()
	return render(request,'services/rolereq.html',{'a':k})
def permissions(request):
	ty=User.objects.all()
	a=RoleRqst.objects.all()
	c,rr=[],{}
	for b in a:
		c.append(b.uid_id)
	for j in ty:
		if j.is_superuser==1 or j.id not in c:
			continue
		else: 
			d=RoleRqst.objects.get(uid_id=j.id)
			rr[j.id]=j.username,d.roletype,j.role,j.id
	e=rr.values()
	return render(request,'services/givepermissions.html',{'q':e})
def giveper(request,k):
	r=User.objects.get(id=k)
	m=RoleRqst.objects.get(uid_id=k)
	if request.method == "POST":
		k=RoleUp(request.POST,instance=r)
		if k.is_valid():
			k.save()
			m.is_checked=1
			m.save()
			return redirect('/permission')
	k= RoleUp(instance=r)
	return render(request,'services/acceptpermissions.html',{'y':k})



def viewuser(request):
	p=User.objects.all()
	return render(request,'services/viewuser.html',{'u':p})

def customer(request,id):
	a=User.objects.get(id=id)
	a.role="2"
	a.save()
	return redirect('/viewuser')

def owner(request,id):
	a=User.objects.get(id=id)
	a.role="1"
	a.save()
	return redirect('/viewuser')

def registration(request):
	if request.method=="POST":
		p=UsForm(request.POST)
		if p.is_valid():
			p.save()
			return redirect('/log')
			
	p=UsForm()
	return render(request,'services/register.html',{'u':p})

def role(request):
	return render(request,'services/role.html')

def addcategory(request):
	if request.method=="POST":
		a=CategoryForm(request.POST)
		if a.is_valid():
			a.save()
			return redirect('/category')
	cf=CategoryForm()
	return render(request,'services/addcategory.html',{'c':cf})

def addcarservices(request):
	if request.method=="POST":
		b=AddForm(request.POST)
		if b.is_valid():
			b.save()
			return redirect('/category')
	se=AddForm()
	return render(request,'services/addcarservices.html',{'e':se})

def infodelete(req,et):
	data=Services.objects.get(id=et)
	if req.method == "POST":
		data.delete()
		return redirect('/showdata')
	return render(req,'services/userdelete.html',{'sd':data})

def userupdate(up,si):
	t=Services.objects.get(id=si)
	if up.method=="POST":
		d=Userupdate(up.POST,instance=t)
		if d.is_valid():
			d.save()
			return redirect('/showdata')
	d=Userupdate(instance=t)
	return render(up,'services/updateuser.html',{'us':d})
def showinfo(req):
	data=Services.objects.all()
	return render(req,'services/showdata.html',{'info':data})


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
	p=Services.objects.filter(sid_id=id)
	paginator=Paginator(p,10)
	page=request.GET.get('page')
	try:
		p=paginator.page(page)
	except PageNotAnInteger:
		p=paginator.page(1)
	except EmptyPage:
		p=paginator.page(paginator.num_pages)
	return render(request,'services/carservices.html',{'da':p,'data':d})

def addcart(request,id):
	b=Services.objects.get(id=id)
	c=Cart(user_id=request.user.id,service_id=id)
	c.save()
	count=0
	data1 = Cart.objects.filter(user_id=request.user.id)
	for i in data1:
		count+=1
	return render(request,'services/addcart.html',{'b':c,'count':count,'data1':data1})

def cartdetails(request):
	c=Cart.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.service.price
	return render(request,'services/cartdetails.html',{'sum':sum,'count':count,'data':d,'cart':c})

def placeorder(request):
	data=Cart.objects.filter(user_id=request.user.id)
	b=request.user.email
	l1=[]
	l2=[]
	sum=0
	count=0
	for i in data:
		sum=sum+i.service.price
		l1.append(i.service.service_type)
	message='service type ::\n'+' ,'.join(l1)+'\n'+ ' will be contact you.\n'+'Total amount paid: Rs.'+str(sum)+'\n'+'THANK YOU for request!!'
	subject='service booked'
	sender=settings.EMAIL_HOST_USER
	if data:
		t=EmailMessage(subject,message,sender,[b])
		t.send()
		for i in data:
			print(i.service.service_type)
			s=Myorders(service_type=i.service.service_type,price=i.service.price,user_id=request.user.id)
			s.save()
		data.delete()
	return render(request,'services/placeorder.html')

def myorders(request):
	my=Myorders.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	sum=0
	count=0
	for i in my:
		count=count+1
		sum=sum+i.price
	return render(request,'services/myorders.html',{'sum':sum,'count':count,'my':my})

def remove(request,id):
	c=Cart.objects.get(id=id)
	c.delete()
	return redirect('/cartdetails')
def custom(request):
	d=CarCategory.objects.all()
	if request.method=="POST":
		j=CustomiseForm(request.POST,request.FILES)
		if j.is_valid():
			subject='Order Confirmed'
			body="thank you "+request.POST['uname']+" we will contact you soon!!!"+'\n'+"Description ::"+request.POST['description']
			receiver=request.POST['email']
			sender=settings.EMAIL_HOST_USER
			t=EmailMessage(subject,body,sender,[receiver])
			t.content_subtype='html'
			t.send()
			j.save()
			messages.success(request,"Successfully sent to your mail ")
			return redirect('/')
	j=CustomiseForm()
	k=Customise.objects.all()
	return render(request,'services/customise.html',{'u':j,'data':d})
def cancle(request):
	my=Myorders.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	b=request.user.email
	l1=[]
	sum=0
	count=0
	for i in my:
		count=count+1
		sum=sum+i.price
		l1.append(i.service_type)
		message='service type ::\n'+' ,'.join(l1)+'\n'+ ' will be contact you.\n'+'Total amount paid: Rs.'+str(sum)+'\n'+'THANK YOU for request!!'
		subject='service cancled'
		sender=settings.EMAIL_HOST_USER
	if i in  my:
		t=EmailMessage(subject,message,sender,[b])
		t.send()
		my.delete()
	return render(request,'services/cancle.html')

	



