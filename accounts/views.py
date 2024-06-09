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
from accounts.serializers import PersonalProfileSerializers, PersonalLocationSerializers, PersonalSocialMediaSerializers, UserSerializer
from accounts.models import PersonalProfile, PersonalSocial, PersonalLocation
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import permissions



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

class ProfileDetail(generics.RetrieveAPIView):
    serializer_class = PersonalProfileSerializers
    queryset = PersonalProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_object_or_404(get_user_model(), id=instance.user.id)
        social = PersonalSocial.objects.filter(user=user)
        social_serializer = PersonalSocialMediaSerializers(social, many=True)
        profileserializer = self.get_serializer(instance)
        
        
        data = {
            "profile": profileserializer.data,
            "social": social_serializer.data
        }
        
        return Response(data)
    
    

class ProfileRetriveUpdateDestroy(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalProfileSerializers
    queryset = PersonalProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_url_kwarg = 'pk'
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user__id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

class PLocationRetriveUpdateDestroy(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalLocationSerializers
    queryset = PersonalLocation.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
class PSocialMediaListCreate(generics.CreateAPIView):
    serializer_class = PersonalSocialMediaSerializers
    queryset = PersonalSocial.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class PSocialMediaRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalSocialMediaSerializers
    queryset = PersonalSocial.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    


class UserMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    

    def get(self, request, format=None):
        
        return Response(self.serializer_class(request.user).data)


class PersonalLocationCreateView(generics.CreateAPIView):
    serializer_class = PersonalLocationSerializers
    queryset = PersonalLocation.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class PersonalLocationRetrieveEditDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalLocationSerializers
    queryset = PersonalLocation.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
