from django.contrib import admin

from .models import *

admin.site.register(Book)
admin.site.register(BorrowBook)
admin.site.register(Fine)
admin.site.register(BorrowLimit)