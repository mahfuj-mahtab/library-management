from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets

class ShowAllBook(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer