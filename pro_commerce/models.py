from django.db import models
from compte.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify

from e_comm import settings

# Create your models here.
class Category(models.Model):
    nom = models.CharField(max_length=40, verbose_name='Nom de la catégorie')
    slug = models.SlugField(unique=True, max_length=255,blank=True)


    class Meta:
        verbose_name = 'Nom de la catégorie'
        verbose_name_plural = 'Catégories'
    # #    
    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.nom)
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(self.nom)}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
class Subcategory(models.Model):
    nom = models.CharField(max_length=40, verbose_name='Nom de la sous-catégorie')
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='souscategories')
    slug = models.SlugField(unique=True, max_length=255,blank=True)

    class Meta:
        verbose_name = 'Sous-catégorie'
        verbose_name_plural = 'Sous-catégories'
   
    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = slugify(self.nom)
            num = 1
            while Subcategory.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slugify(self.nom)}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
#
class Product(models.Model):
    photo = models.ImageField(upload_to='products/', verbose_name='Photo du produit')
    nom = models.CharField(max_length=40, verbose_name='Nom du produit')
    ville=models.CharField(max_length=200,verbose_name='ville du produit')
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
    produit= models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='produit',related_name='produit')
    def __str__(self):
        return f"{self.ville}, {self.quartier}, {self.repere} - {self.utilisateur.username}"
#

class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')