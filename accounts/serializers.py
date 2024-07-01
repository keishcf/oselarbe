from .models import PersonalProfile, PersonalLocation, PersonalSocial, FavoriteBusiness
from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
import business.models as biz_models


class PersonalLocationSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = PersonalLocation
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
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class PersonalProfileSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # profile_picture = serializers.SerializerMethodField("get_profile_picture")
    # location = PersonalLocationSerializers(many=False)
    class Meta:
        model = PersonalProfile
        fields = ["user", "profile_picture", "bio", "phone", "hometown", "primary_language", "web_url", "country"]
    


class FavoriteBusinessViewSerializers(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = biz_models.BusinessProfile
        fields = ["id", "name", "logo", "description", "country", "is_verified"]
        
    def get_logo(self, obj):
        if obj.media.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.media.logo.url)
        return None
            

class FavoriteBusinessSerializer(serializers.ModelSerializer):
    business = FavoriteBusinessViewSerializers()
    class Meta:
        model = FavoriteBusiness
        fields = "__all__"
        
class FavoriteBusinessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBusiness
        fields = "__all__"