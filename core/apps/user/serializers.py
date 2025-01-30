from rest_framework import serializers
from apps.user.models import CustomUser
from apps.book.serializers import BookBorrowSerializer
class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BookBorrowSerializer(many = True,read_only=True)
    class Meta:
        model = CustomUser
        exclude = ('password',)
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_type', 'avatar', 'password', 'first_name','last_name']
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.username = validated_data['email'].split('@')[0]
        user.save()
        return user