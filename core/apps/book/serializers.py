from rest_framework import serializers
from .models import *
from apps.author.serializers import *
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
         model = Book
         fields = '__all__'
class BookBorrowSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    book = BookSerializer()
    class Meta:
         model = BorrowBook
         fields = '__all__'
class FineSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    book = BookSerializer()
    class Meta:
         model = Fine
         fields = '__all__'