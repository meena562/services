from django.shortcuts import render,redirect
from service.forms import UsForm,Userupdate,ChpwdForm,UpdPfle,CategoryForm,AddForm,CustomiseForm,RoleR,RoleUp,CancelForm
from django.core.mail import send_mail
from carservice import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from service.models import User,CarCategory,Services,Cart,Myorders,Customise,RoleRqst
from django.core.mail import send_mail,EmailMessage
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login
import tempfile
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here
def home(request):
	cf=CarCategory.objects.all()
	return render(request,'services/home.html',{'data':cf})
def Login_valid(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)

		if not user:
			messages.add_message(request,messages.WARNING,'invalid Credentials chech your password and username once')
			return render(request,'services/login.html')
		else:
			login(request,user)
			messages.add_message(request,messages.SUCCESS,f'Welcome {user.username}')
			return redirect('/')
	return render(request,'services/login.html')
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
def vieworders(request):
	o=Myorders.objects.all()
	return render(request,'services/vieworders.html',{'s':o})

def customer(request,id):
	a=User.objects.get(id=id)
	a.role="2"
	a.save()
	return redirect('/viewuser')
def serpending(request,id):
	a=Myorders.objects.get(id=id)
	a.is_status="1"
	a.save()
	return redirect('/vieworders')

def owner(request,id):
	a=User.objects.get(id=id)
	a.role="1"
	a.save()
	return redirect('/viewuser')
def serprovided(request,id):
	a=Myorders.objects.get(id=id)
	a.is_status="0"
	a.save()
	return redirect('/vieworders')
def date(request,id):
	a=User.objects.get(id=id)
	return render(request,)


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

def cgf(request):
	if request.method=="POST":
		c=ChpwdForm(user=request.user,data=request.POST)
		if c.is_valid():
			c.save()
			return redirect('/log')
	c=ChpwdForm(user=request)
	return render(request,'services/changepassword.html',{'t':c})	

def updprofile(request):
	if request.method == "POST":
		t = UpdPfle(request.POST,instance=request.user)
		if t.is_valid():
			t.save()
			return redirect('/profile')
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
	if request.method=="POST":
		c=Cart(user_id=request.user.id,service_id=id)
		c.save()
		return redirect('/cartdetails')
	return render(request,'services/addcart.html')

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
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.service.price
	return render(request,'services/placeorder.html',{'sum':sum,'count':count,'cart':c})
def msg(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.veg.price
	return render(request,'services/message.html',{'count':count})


def msg1(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.veg.price
	return render(request,'services/message1.html',{'count':count})

def msg2(request):
	
	return render(request,'services/msg2.html')

def myorders(request):
	my=Myorders.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	sum=0
	count=0
	for i in my:
		count=count+1
		sum=sum+i.price
	return render(request,'services/myorders.html',{'sum':sum,'count':count,'my':my,'data':d})

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
def checkout(request):
	c=Cart.objects.filter(user_id=request.user.id)
	
	if request.method=="POST":
		m=request.user.email
		receiver=m
		l=[]
		x=[]
		sum=0
		for i in c:
			sum=sum+i.service.price
			l.append(i.service.service_type)
				
		message='Ordered services ::\n'+' ,'.join(l) +'\n'+'service will be provided within 5 days.'+'\n'+'Total amount paid: Rs.'+str(sum)+'\n'+'THANK YOU !! \n'
		subject='Order confirmed'
		st=settings.EMAIL_HOST_USER
		if c:
			at=send_mail(subject,message,st,[receiver])
				
			for i in x:
				at.attach(i.name,i.read())
				at.send()
			for i in c:
				sum=sum+i.service.price
				a=Myorders(service_type=i.service.service_type,price=i.service.price,user_id=request.user.id)
				a.save()
				he=Services.objects.filter(id=i.service_id)
				for i in he:
					i.save()
			c.delete()
			return redirect('msg')
		return redirect('msg1')
		
	
	return render(request,'html/placeorder.html')
	
def cancel(request,si):
	d=CarCategory.objects.all()
	x=Myorders.objects.get(id=si)
	j=CancelForm(request.POST,instance=x)
	if request.method=="POST":
		if j.is_valid():
			receiver=request.user.email
			sender=settings.EMAIL_HOST_USER
			subject="order cancelled"
			body="thank you "+'\n'+"your order has been cancelled"+'\t'+request.POST['service_type']
			send_mail(sender,body,subject,[receiver])
			j.save()
			return HttpResponse('Your order has been cancelled')
			he=Product.objects.filter(id=i.service_id)
			for i in he:
				i.save()
		x.delete()
	j=CancelForm(instance=x)
	return render(request,'services/cancel.html',{'data':d,'prod':j})
def appointment(request):
	my=Myorders.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	sum=0
	count=0
	for i in my:
		count=count+1
		sum=sum+i.price
	return render(request,'services/appointment.html',{'sum':sum,'count':count,'my':my})
def search(request):
	try:
		q=request.GET.get('q')
	except:
		q=None
	if q:
		p1=Services.objects.filter(service_type__icontains=q)
		context={'d':p1}
		template="services/search.html"
	else:
		message="Search for a specific service Name"
		context={'empty':True,'message':message}
		template="services/search.html"
	return render(request,template,context)
def pdf(request):
	c=Cart.objects.filter(user_id=request.user.id)
	d=CarCategory.objects.all()
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.service.price
	template_path="services/pdfpage.html"
	dic={}
	for i in c:
		dic[i.id]=i.service.service_type,i.service.price
	var=dic.values()
	dic2={'var':var,'sum':sum}
	response=HttpResponse(content_type="application/pdf")
	response["Content-Disposition"]="attachment;filename='productsreport.pdf'"
	template=get_template(template_path)
	html=template.render(dic2)
	pisa_status=pisa.CreatePDF(html,dest=response)
	if pisa_status.err:
		return HttpResponse("wrong")
	return response



