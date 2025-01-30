from django.db import models
from apps.user.models import CustomUser
class Author(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='CustomUser')  
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
