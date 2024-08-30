from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Man'),
        ('W', 'Woman'),
    ]

    email = models.EmailField(blank=False, null=False)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(default='M', choices=GENDER_CHOICES, max_length=1)
    stats = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='cover/profile/')
    
    def __str__(self):
        return self.username


