from django.db import models

# Create your models here.
from django.contrib.auth.models import User,AbstractUser

class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('MEMBER', 'MEMBER'),
    )
    avatar = models.TextField(blank=True, null=True,default='default.jpg')
    user_type = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='member')
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )
    def __str__(self):
        return self.username