from django import forms
from .models import Product, Category, ReviewRating, Subcategory,Adresse
from phonenumber_field.formfields import PhoneNumberField

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['photo', 'nom', 'ville', 'description', 'prix', 'stock', 'categorie', 'sous_categorie','adresse']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'sous_categorie': forms.Select(attrs={'class': 'form-control'}),
                        'adresse': forms.Select(attrs={'class': 'form-control'}),


        }

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) > 40:
            raise forms.ValidationError("Le nom du produit ne peut pas dépasser 40 caractères.")
        return nom

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix <= 0:
            raise forms.ValidationError("Le prix doit être un nombre positif.")
        return prix

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Le stock ne peut pas être négatif.")
        return stock
    #
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['adresse'].queryset = Adresse.objects.filter(utilisateur=user)
    #ADRESSE FORM

class AdresseForm(forms.ModelForm):
    contact = PhoneNumberField()

    class Meta:
        model = Adresse
        fields = ['ville', 'quartier', 'repere', 'contact']
        
        widgets = {
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la ville'}),
            'quartier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le quartier'}),
            'repere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le point de référence'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de téléphone'}),
        }
    
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        # Ensure contact is valid
        if not contact:
            raise forms.ValidationError("Le numéro de téléphone est requis.")
        return contact
    
    def clean_ville(self):
        ville = self.cleaned_data.get('ville')
        # Ensure ville is not empty
        if not ville:
            raise forms.ValidationError("La ville est requise.")
        return ville
    
    def clean_quartier(self):
        quartier = self.cleaned_data.get('quartier')
        # Ensure quartier is not empty
        if not quartier:
            raise forms.ValidationError("Le quartier est requis.")
        return quartier
    
    def clean_repere(self):
        repere = self.cleaned_data.get('repere')
        # Ensure repere is not empty
        if not repere:
            raise forms.ValidationError("Le point de référence est requis.")
        return repere
    
    def clean_produit(self):
        produit = self.cleaned_data.get('produit')
        # Ensure produit is selected
        if not produit:
            raise forms.ValidationError("Le produit est requis.")
        return produit
#

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']