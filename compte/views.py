from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings

from compte.models import User
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_page(request):
    form= forms.LoginForm()
    message = ''

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
     
    # Vérifiez si l'utilisateur est authentifié avant de l'inclure dans le contexte
    context = {
        'form': form,
        'message': message,
        }
     # Ajouter un log pour vérifier l'utilisateur
    print(f"Request User: {request.user} - Authenticated: {request.user.is_authenticated}")


    return render(request,'compte/login.html',context)

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
#profile user
@login_required
def profile(request):
    return render(request,'compte/profile_user.html')

def profile(request):
    profile = User.objects.get(username=request.user)
    form = forms.UserProfileForm(instance=profile)

    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            # Rediriger
            return redirect('pro_commerce:homepage') 
#  vers la page de profil avec un message de succès

    return render(request, 'compte/profile_user.html', {'form': form, 'profile': profile})