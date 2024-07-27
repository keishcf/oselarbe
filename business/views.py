from django.shortcuts import render, get_object_or_404
import business.serializers as biz_serializers
from rest_framework import generics
from rest_framework.views import APIView
import business.models as biz_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action


class BusinessViewSet(viewsets.GenericViewSet):
    serializer_class = biz_serializers.BusinessSerializers
    queryset = biz_model.BusinessProfile.objects.all()
    lookup_field = 'slug'
    
    def list(self, request, *args, **kwargs):
        serializer = biz_serializers.BusinessSerializers(self.get_queryset(), context={'request': request}, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.serializer_class(queryset, context={'request': request})

        weighted_average = biz_model.BusinessReview.get_weighted_average(queryset)
        hours_serializer = biz_serializers.BusinessHoursSerializers(queryset.hours.all(), many=True)
        serializer_data = serializer.data
        serializer_data['phone'] = queryset.contact.phone
        serializer_data['email'] = queryset.contact.email
        serializer_data['website'] = queryset.contact.website
        serializer_data['hours'] = hours_serializer.data
        # serializer_data['message'] = queryset.short_message.message
        data = {
            "profile": serializer_data,
            "stastics": {
                "weighted_average": round(weighted_average, 1),
                "review_count": queryset.reviews_count
            },
        }
        return Response(data)

    
class ReviewViewSet(viewsets.GenericViewSet):
    serializer_class = biz_serializers.BusinessReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return biz_model.BusinessReview.objects.get(pk=self.kwargs['pk'])
    
    def get_queryset(self):
        return biz_model.BusinessReview.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'mark_helpful']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        review = self.get_object()
        serializer = self.serializer_class(review, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        review = biz_model.BusinessReview.objects.get(pk=pk)
        self.check_object_permissions(request, review)
        serializer = self.serializer_class(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def write_review(self, request, pk=None):
        user = request.user
        business = get_object_or_404(biz_model.BusinessProfile, id=pk)
        serializers = biz_serializers.BusinessReviewSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(business=business, user=user)
            return Response({"message": "Review Successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        user = request.user
        review = self.get_object()
        
        helpful_reaction, created = biz_model.ReviewHelpful.objects.get_or_create(user=user, review=review, helpful=True)
        
        if created:
            return Response({"message": "Marked as helpful"}, status=status.HTTP_201_CREATED)
        elif helpful_reaction.helpful:
            helpful_reaction.delete()
            return Response({"message": "Removed helpful mark"}, status=status.HTTP_200_OK)
    
    
    
    
    