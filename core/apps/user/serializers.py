from rest_framework import serializers
from apps.user.models import User
from apps.book.serializers import *
class UserSerializers(serializers.ModelSerializer):
    borrowed_books = BookBorrowSerializer(many = True)
    class Meta:
        model = User
        exclude = ('password',)
