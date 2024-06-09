from .models import PersonalProfile, PersonalLocation, PersonalSocial
from rest_framework import serializers
from django.contrib.auth import get_user_model


class PersonalLocationSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = PersonalLocation
        fields = '__all__'

class PersonalProfileSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # location = PersonalLocationSerializers(many=False)
    class Meta:
        model = PersonalProfile
        fields = '__all__'
         
        
class PersonalSocialMediaSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = PersonalSocial
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'is_business', 'is_personal')
        
