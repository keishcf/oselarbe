from django.shortcuts import render
from .serializers import BusinessCategoriesSerializers
from rest_framework import generics
from .models import BusinessCategory
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class ListBusinessCategory(generics.ListAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategoriesSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]