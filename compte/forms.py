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
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label="Nouveau mot de passe",
        required=False
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmer le mot de passe",
        required=False
    )
    
    
    class Meta:
        model = User
        fields = ['username', 'photo','telephone']
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            # 'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'confirmer_mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),



            
        }
    def clean(self):
            cleaned_data = super().clean()
            new_password = cleaned_data.get('nouveau_mot_de_passe')
            confirm_password = cleaned_data.get('confirmer_mot_de_passe')

            if new_password and new_password != confirm_password:
                self.add_error('confirmer_mot_de_passe', "Les mots de passe ne correspondent pas.")

            return cleaned_data