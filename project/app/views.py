from django.shortcuts import render, redirect
from django.contrib import messages
from enroll.models import User
from django.contrib.auth.models import User as mu
from django.contrib.auth import authenticate
# from django.contrib.auth import login,logout
from django.views.decorators.cache import never_cache



# Create your views here.


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@never_cache
def base(request):
    if 'username' in request.session:
        return render(request, 'base.html')
    
    return redirect('handlelogin')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password_1']
        confirmpassword = request.POST['password_2']
        
        if password == confirmpassword:
            if User.objects.filter(name=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('signup')
            else:
                myuser=User(name=username,email=email,password=password)
                myuser.save()
                messages.success(request,'signup success, please login')
                return redirect('handlelogin')
        else:
            messages.warning(request, 'Password not matching')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request,'signup.html')

def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password_1']

        superuser_name = mu.objects.filter(is_superuser=True).values('username')[0]['username']
        if superuser_name == username and User.objects.filter(password=password).exists():
            request.session['username'] = superuser_name
            if request.session.get('username') == superuser_name:
                # request.session.flush()
                return redirect('/dashboard')
        if User.objects.filter(name=username).exists() and User.objects.filter(password=password).exists():
            request.session['username'] = username
            if request.session.get('username') == username:
                messages.success(request,'login success')
                return redirect('/base')
        else:
            messages.error(request,'inavalid credentials')
            return redirect('handlelogin')
        
    superuser_name = mu.objects.filter(is_superuser=True).values('username')[0]['username']
    if request.session.get('username') == superuser_name:
        return redirect('/dashboard')
    if request.session.get('username'):
        return redirect('/base')
    return render(request,'login.html')

def handlelogout(request):
    if 'username' in request.session:
        request.session.flush()
        messages.info(request,'logout success')
    return redirect('handlelogin')