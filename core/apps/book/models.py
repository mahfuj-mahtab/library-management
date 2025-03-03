from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.author.models import *
from apps.user.models import *
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BorrowBook(models.Model):
    status = [
        ('APPROVED','APPROVED'),
        ('RETURNED','RETURNED'),
        ('HOLD','HOLD'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_deadline = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.TextField(choices=status,default = 'APPROVED')
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.return_deadline:
            self.return_deadline = timezone.now() + timedelta(days=14)
        
        if self.status == 'RETURNED' and self.returned_at:
            late_days = (self.returned_at - self.return_deadline).days
            fine_per_day = 5.00  
            self.fine = late_days * fine_per_day
            self.status = 'HOLD'

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
    

class BorrowLimit(models.Model):
    limit = models.PositiveIntegerField(default=5)

    def __str__(self):
        return 'limit'