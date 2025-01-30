from rest_framework import serializers
from .models import *
from apps.author.serializers import *
from apps.user.serializers import *
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
         model = Book
         fields = '__all__'
class BookBorrowSerializer(serializers.ModelSerializer):
    # user = UserSerializers()
    class Meta:
         model = BorrowBook
         fields = '__all__'
class FineSerializer(serializers.ModelSerializer):
    # user = UserSerializers()
    class Meta:
         model = Fine
         fields = '__all__'