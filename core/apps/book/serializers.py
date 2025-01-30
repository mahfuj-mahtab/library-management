from rest_framework import serializers
from .models import *
from apps.author.serializers import *
from apps.user.serializers import *
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)
    class Meta:
         model = Book
         fields = '__all__'
class BookBorrowSerializer(serializers.ModelSerializer):
    # user = UserSerializers()
    class Meta:
         model = BorrowBook
         fields = '__all__'
