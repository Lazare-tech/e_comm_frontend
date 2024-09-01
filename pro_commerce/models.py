from django.db import models
from compte.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.db.models import Avg, Count
from e_comm import settings

# Create your models here.
class Category(models.Model):
    nom = models.CharField(max_length=40, verbose_name='Nom de la catégorie')
    slug = models.SlugField(unique=True, max_length=255,blank=True)
    photo = models.ImageField(upload_to='category_images/', verbose_name='Photo du categorie',blank=True,null=True)

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
    photo = models.ImageField(upload_to='sub_category_images/', verbose_name='Photo du sous categorie',blank=True,null=True)

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
 
class Adresse(models.Model):
    ville = models.CharField(max_length=40, verbose_name='Ville du vendeur')
    quartier = models.CharField(max_length=40, verbose_name='Quartier ou secteur du vendeur')
    repere = models.CharField(max_length=40, verbose_name='Point de référence du vendeur')
    contact = PhoneNumberField(verbose_name='Numéro de téléphone')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Utilisateur', related_name='adresses')
    def __str__(self):
        return f"{self.ville}, {self.quartier}, {self.repere} - {self.utilisateur.username}"
#
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
    adresse= models.ForeignKey(Adresse,on_delete=models.CASCADE,verbose_name='adresse',related_name='adresse',null=True)

   
    def __str__(self):
        return self.nom
    def averageReview(self):
        reviews = ReviewRating.objects.filter(produit=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(produit=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
#
class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
#
class ReviewRating(models.Model):
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True,null=True)
    review = models.TextField(max_length=500, blank=True,null=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
# #---------------------------------------------
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produit.header}: {self.rating}"