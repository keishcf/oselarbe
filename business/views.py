from django.shortcuts import render
from .serializers import BusinessCategoriesSerializers, BusinessReviewSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .models import BusinessCategory
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ListBusinessCategory(generics.ListAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategoriesSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class BusinessReviewView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    paginate_by = 1
    serializer_class = BusinessReviewSerializer
    def get_queryset(self):
        user_reviews = self.request.user.reviews.all()
        return user_reviews