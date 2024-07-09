from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings
from . import forms
# Create your views here.
def login_page(request):
   form= forms.LoginForm()
   message = ''
   user=request.user

   if request.method== 'POST':
       form= forms.LoginForm(request.POST)
       if form.is_valid():
           user= authenticate(
               username= form.cleaned_data['username'],
               password= form.cleaned_data['password']
           )
           if user is not None:
               login(request,user)
               return redirect('pro_commerce:homepage')
           
       message='invalid credentials'
   return render(request,'compte/login.html',context={'form':form,'message':message,'user':user})

#vue dinscription
def signup_page(request):
    form = forms.SignupForm()
    if request.method== 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,'compte/signup.html',context={'form':form})
#deconnexion
def logout_user(request):
    logout(request)
    
    return redirect('pro_commerce:homepage')