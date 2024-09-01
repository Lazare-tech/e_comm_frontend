from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True,verbose_name="Numero de telephone")
    photo = models.ImageField(upload_to='profile_photo/', verbose_name='Photo de profile',blank=True,null=True)

