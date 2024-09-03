from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings

from compte.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


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

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('nouveau_mot_de_passe'):
                update_session_auth_hash(request, user)  # Met à jour la session pour éviter la déconnexion
            # messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('pro_commerce:homepage')
    else:
        form = forms.UserProfileForm(instance=user)
    
    return render(request, 'compte/profile_user.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('pro_commerce:homepage')  # Redirigez vers une page d'accueil ou de connexion après suppression
    return redirect('compte:profile')