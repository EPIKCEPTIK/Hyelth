from django.contrib.auth.models import *
from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medicines/')
    expiration = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    medicines = models.TextField(default="{}",blank=True)