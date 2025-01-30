from rest_framework import serializers
from .models import *
from apps.user.serializers import *

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    class Meta:
         model = Author
         fields = '__all__'