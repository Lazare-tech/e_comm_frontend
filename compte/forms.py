# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from compte.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')
#
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields=('username','telephone')
#
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'email','photo','password','telephone']
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirmer_mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),



            
        }
