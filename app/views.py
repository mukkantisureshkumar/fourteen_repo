from django.shortcuts import render
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
# Create your views here.
def register(request):
    eufo=UserForm()
    epfo=ProfileForm()
    d={'k1':eufo,'k2':epfo}
    if request.method=='POST' and request.FILES:
        ufcd=UserForm(request.POST)
        pfcd=ProfileForm(request.POST,request.FILES)
        if ufcd.is_valid() and pfcd.is_valid():
            mufd=ufcd.save(commit=False)
            pw=ufcd.cleaned_data['password']
            mufd.set_password(pw)
            mufd.save()
            mpfd=pfcd.save(commit=False)
            mpfd.username=mufd
            mpfd.save()

            send_mail(
                'registration',
                'thank you for registration!',
                'mukkantisureshkumar777@gmail.com',
                [mufd.email],
                fail_silently=False,
                
            )
            return HttpResponse('registration successfull')
        else:
            return HttpResponse('invalid registratin')
    return render(request,'register.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request, "home.html")



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        auo=authenticate(username=username,password=password)
        if auo and auo.is_active:
            login(request,auo)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid user credentials')
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    u_n=request.session.get('username')
    UO=User.objects.get(username=u_n)

    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pww=request.POST['pw']
        un=request.session.get('username')
        uo=User.objects.get(username=un)
        uo.set_password(pww)
        uo.save()
        return HttpResponse('change password successfully')
    return render(request,'change_password.html')