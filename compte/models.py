from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)

