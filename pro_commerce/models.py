from django.db import models
from compte.models import User
from phonenumber_field.modelfields import PhoneNumberField

from e_comm import settings

# Create your models here.
class Category(models.Model):
    nom = models.CharField(max_length=40, verbose_name='Nom de la catégorie')

    class Meta:
        verbose_name = 'Nom de la catégorie'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.nom

class Subcategory(models.Model):
    nom = models.CharField(max_length=40, verbose_name='Nom de la sous-catégorie')
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='souscategories')

    class Meta:
        verbose_name = 'Sous-catégorie'
        verbose_name_plural = 'Sous-catégories'

    def __str__(self):
        return self.nom
class Product(models.Model):
    photo = models.ImageField(upload_to='products/', verbose_name='Photo du produit')
    nom = models.CharField(max_length=40, verbose_name='Nom du produit')
    description = models.TextField(verbose_name='Description du produit')
    prix = models.BigIntegerField(verbose_name='Prix du produit')
    stock = models.BigIntegerField(verbose_name='Stock disponible du produit')
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Catégorie du produit', related_name='produits')
    sous_categorie=models.ForeignKey(Subcategory,on_delete=models.CASCADE,verbose_name='sous categorie produit',related_name='souscategorieduproduit',blank=True,null=True)
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='produit de utilisateur', related_name='produituser')

   
    def __str__(self):
        return self.nom
    
class Adresse(models.Model):
    ville = models.CharField(max_length=40, verbose_name='Ville du vendeur')
    quartier = models.CharField(max_length=40, verbose_name='Quartier ou secteur du vendeur')
    repere = models.CharField(max_length=40, verbose_name='Point de référence du vendeur')
    contact = PhoneNumberField(verbose_name='Numéro de téléphone')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Utilisateur', related_name='adresses')

    def __str__(self):
        return f"{self.ville}, {self.quartier}, {self.repere} - {self.utilisateur.username}"
