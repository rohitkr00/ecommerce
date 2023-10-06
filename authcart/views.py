from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def generateOTP(n):
		range_start = 10**(n-1)
		range_end = (10**n)-1
		return randint(range_start, range_end)

def sendemail(email, otp):
	try:
		message = """
					<html>
					<body>
					<h1>Login OTP</h1>
					<hr>
					<h3>Your login otp is {0} , please don't share it with anayone</h3>
					<br>
					<h2>Thank You</h2>
					</body>
					</html>""".format(otp)
		msg=MIMEMultipart()
		msg['Subject'] = "Login otp"
		msg['From'] = "manankr21@gmail.com"
		msg['To'] = email
		msg.attach(MIMEText(message,'html'))

		smtp = smtplib.SMTP(host='smtp.gmail.com',port=587)
		smtp.starttls()
		smtp.login("manankr21@gmail.com","pdbqfdfbeoxfuuca")
		smtp.send_message(msg)
		smtp.quit()
		return True

	except Exception as ex:
		print("Mail send Error : ",ex)
		return False

def signupf(request):
     return render(request,"signup.html")

def signup(request):
    if (request.method=="GET"):
        global email
        global password
        email=request.GET['email']
        password=request.GET['pass1']
        confirm_password=request.GET['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is not matching")
            return render(request,"signup.html")
        
        # try:
        # if User.objects.get(username=email):
        #     messages.info(request,"Email is taken")
        #     return render(request,"signup.html")
            #return HttpResponse("email already exist")
        
        # except Exception as identifier:
        #     pass

        global otp2

        otp2=generateOTP(5)
        print(otp2)
        check = sendemail(email,otp2)
        print(check)      
        # user = User.objects.create_user(email,email,password)
        # user.is_active=True
        # user.save()
        # messages.success(request,"Signup Succesful")
        # email_subject="Activate Your Account"
        # message1=render_to_string('activate.html',{
        #     'user':user,
        #     'domain':'127.0.0.1:8000',
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token':generate_token.make_token(user)
        # })
        
        # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        # email_message.send()
        # messages.success(request,"Activate Your Account by clicking the link in your gmail")
        # return redirect('auth/login/')

        # message = message1
        # msg=MIMEMultipart()
        # msg['Subject'] = email_subject
        # msg['From'] = "manankr21@gmail.com"
        # msg['To'] = email
        # msg.attach(MIMEText(message,'html'))

        # smtp = smtplib.SMTP(host='smtp.gmail.com',port=587)
        # smtp.starttls()
        # smtp.login("manankr21@gmail.com","tuaafayrfuegbgbh")
        # smtp.send_message(msg)
        # smtp.quit()
        # return True

    return render(request,"verf.html")

def OTPverf(request):
        otp1=request.GET["otp3"]
        print(otp1)
        if int(otp1)==otp2:
            user = User.objects.create_user(email,email,password)
            user.is_active=True
            user.save()
            messages.success(request,"Signup Succesful")
            return render(request,"login.html")  
        else:
            messages.warning(request,"login failed")
            return render(request,"signup.html")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Succesfully")
            return redirect('/auth/login')
        return render(request,'activatefail.html')

def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login')
        


    return render(request,"login.html")

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login')


