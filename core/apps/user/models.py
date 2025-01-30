from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('MEMBER', 'MEMBER'),
    )
    avatar = models.TextField(blank=True, null=True,default='default.jpg')
    user_type = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='MEMBER')

    def __str__(self):
        return self.username