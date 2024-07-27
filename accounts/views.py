from django.shortcuts import render, get_object_or_404
from authemail.views import Login, Signup
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.conf import settings
from authemail.models import SignupCode
from authemail.models import send_multi_format_email
from ipware import get_client_ip
from rest_framework import viewsets
from rest_framework.views import APIView
import accounts.serializers as pa_serializers
from accounts.models import PersonalProfile, PersonalSocial, PersonalLocation, PersonalAccount, FavoriteBusiness
from rest_framework.decorators import action
import business.serializers as biz_serializers
import business.models as biz_models
from rest_framework import generics
from rest_framework import permissions
from http import HTTPMethod

from business.paginations import CustomPagination



class BusinessSignupView(Signup):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']

            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

            try:
                user = get_user_model().objects.get(email=email)
                if user.is_verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Delete old signup codes
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_business_account(email=email)

            # Set user fields provided
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            if not must_validate_email:
                user.is_verified = True
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
            user.save()

            if must_validate_email:
                # Create and associate signup code
                client_ip = get_client_ip(request)[0]
                if client_ip is None:
                    client_ip = '0.0.0.0'    # Unable to get the client's IP address
                signup_code = SignupCode.objects.create_signup_code(user, client_ip)
                signup_code.send_signup_email()

            content = {'email': email, 'first_name': first_name,
                       'last_name': last_name}
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonalSignupView(Signup):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']

            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

            try:
                user = get_user_model().objects.get(email=email)
                if user.is_verified:
                    content = {'detail': _('Email address already taken.')}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Delete old signup codes
                    signup_code = SignupCode.objects.get(user=user)
                    signup_code.delete()
                except SignupCode.DoesNotExist:
                    pass

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_personal_account(email=email)

            # Set user fields provided
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            if not must_validate_email:
                user.is_verified = True
                send_multi_format_email('welcome_email',
                                        {'email': user.email, },
                                        target_email=user.email)
            user.save()

            if must_validate_email:
                # Create and associate signup code
                client_ip = get_client_ip(request)[0]
                if client_ip is None:
                    client_ip = '0.0.0.0'    # Unable to get the client's IP address
                signup_code = SignupCode.objects.create_signup_code(user, client_ip)
                signup_code.send_signup_email()

            content = {'email': email, 'first_name': first_name,'last_name': last_name}
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = pa_serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get(self, request, format=None):
        
        return Response(self.serializer_class(request.user).data)

  
class PersonalProfileAccountViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return get_object_or_404(PersonalProfile, user__id=self.request.user.id)
    
    def get_queryset(self):
        return PersonalProfile.objects.all()
    
    
    def list(self, request):
        queryset = get_object_or_404(PersonalProfile, user=self.request.user)
        serializer = pa_serializers.PersonalProfileSerializers(queryset, context={'request': request})
        data = serializer.data
        data["first_name"] = queryset.user.first_name
        data["last_name"] = queryset.user.last_name
        data["date_joined"] = queryset.user.date_joined
        # data["profile_picture"] = request.build_absolute_uri(obj.profile_picture)
        
        
        return Response(data)
    
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(PersonalProfile, user_id=pk)
        serializer = pa_serializers.PersonalProfileSerializers(queryset, context={'request': request})
        data = serializer.data
        data["first_name"] = queryset.user.first_name
        data["last_name"] = queryset.user.last_name
        data["date_joined"] = queryset.user.date_joined
        
        
        return Response(data)
    
    def get_permissions(self):
        if self.action in ['retrieve', 'user_reviews', 'favorites', 'get_user_statistics']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else: 
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=[HTTPMethod.PATCH])
    def change_profile(self, request, *args, **kwargs):
        user = self.request.user
        first_name = self.request.data.get("first_name")
        last_name = self.request.data.get("last_name")
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        user_profile = self.get_object()
        user_serializer = pa_serializers.PersonalProfileSerializers(user_profile, data=self.request.data, context={'request': request})
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, pagination_class=CustomPagination)
    def user_reviews(self, request, pk=None):
        user = get_object_or_404(PersonalAccount, id=pk)
        reviews = user.reviews.all()

        # Apply pagination
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = biz_serializers.BusinessReviewSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = biz_serializers.BusinessReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, pagination_class=CustomPagination)
    def favorites(self, request, pk=None):
        user = get_object_or_404(PersonalAccount, id=pk)
        user_favorite_business = user.favorites.all()
        serializer = pa_serializers.FavoriteBusinessSerializer(user_favorite_business, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=[HTTPMethod.POST])
    def add_to_favorite(self, request, pk=None):
        user = self.request.user
        business = get_object_or_404(biz_models.BusinessProfile, id=pk)
        
        # Check if the favorite already exists for the user and business
        existing_favorite = FavoriteBusiness.objects.filter(personal=user.id, business=business.id).first()
        
        serializer = pa_serializers.FavoriteBusinessCreateSerializer(data={'personal': user.id, 'business': business.id})
        if existing_favorite:
            existing_favorite.delete()  # Delete existing favorite if found
            return Response({"message":"Deletes from Favorite"}, status=status.HTTP_200_OK)
        elif serializer.is_valid():
            serializer.save()
            return Response({"message":"Business Added to Favorite"}, status=status.HTTP_201_CREATED)
    
    # @action(detail=True, methods=HTTPMethod.POST)
    # def mark_helpful(self, request, *args, **kwargs):
    #     review = self.get_object()
    #     user = request.user

    #     # Check if the user has already marked this review as helpful
    #     helpful_instance, created = biz_models.ReviewHelpful.objects.get_or_create(user=user, review=review)

    #     if created or not helpful_instance.marked_helpful:
    #         helpful_instance.marked_helpful = True
    #         helpful_instance.save()
    #         return Response({'status': 'Marked as helpful'})
    #     else:
    #         return Response({'status': 'Already marked as helpful'})

    # @action(detail=True, methods=['post'])
    # def unmark_helpful(self, request, pk=None):
    #     review = self.get_object()
    #     user = request.user

    #     # Check if the user has marked this review as helpful
    #     try:
    #         helpful_instance = biz_models.ReviewHelpful.objects.get(user=user, review=review, marked_helpful=True)
    #         helpful_instance.marked_helpful = False
    #         helpful_instance.save()
    #         return Response({'status': 'Unmarked as helpful'})
    #     except biz_models.ReviewHelpful.DoesNotExist:
    #         return Response({'status': 'Not marked as helpful'})
        
    
    @action(detail=True)
    def get_user_statistics(self, request, pk=None):
        user = get_object_or_404(PersonalAccount, pk=pk)
        total_reviews_number = user.reviews.count()
        total_one_star_reviews = user.reviews.filter(rating=1).count()
        total_two_star_reviews = user.reviews.filter(rating=2).count()
        total_three_star_reviews = user.reviews.filter(rating=3).count()
        total_four_star_reviews = user.reviews.filter(rating=4).count()
        total_five_star_reviews = user.reviews.filter(rating=5).count()
        result = {
            "rating": {
                "OneStar": total_one_star_reviews,
                "TwoStar": total_two_star_reviews,
                "ThreeStar": total_three_star_reviews,
                "FourStar": total_four_star_reviews,
                "FiveStar": total_five_star_reviews,
            },
            "totalReviewsNumber": user.profile.reviews_count,
            "reactions": {
                "helpful": user.profile.helpful_count,
            }
            
        }
        return Response(result, status=status.HTTP_200_OK)