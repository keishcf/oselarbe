from rest_framework import serializers
import business.models as biz_model 

class BusinessCategoriesSerializers(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = biz_model.BusinessCategory
        fields = '__all__'
        debth = 2
        
class BusinessSerializers(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    categories = serializers.StringRelatedField(many=True)
    # review_count = serializers.SerializerMethodField()
    user_favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = biz_model.BusinessProfile
        fields = "__all__"
        
    def get_logo(self, obj):
        request = self.context.get('request')
        logo_url = obj.media.logo.url
        returning_url = request.build_absolute_uri(logo_url)
        return returning_url
    
    def get_user_favorite(self, obj):
        request = self.context.get('request')
        user = request.user
        if(obj.favorite_of.filter(personal=user).exists()):
            return True
        else: return False
        

class BusinessReviewSerializer(serializers.ModelSerializer):
    # business_logo = serializers.SerializerMethodField()
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    business = serializers.SerializerMethodField(read_only=True)
    
    user_marked_helpful = serializers.SerializerMethodField()
    
    class Meta:
        model = biz_model.BusinessReview
        fields = ["id", "rating", "title", "review", "created_at", "updated_at", "business", "helpful_count", "user", "user_marked_helpful"]
        
    def get_business(self, obj):
        request = self.context.get('request')
        data = {
            "reviews_number": obj.business.reviews_count,
            "name": obj.business.name,
            "slug": obj.business.slug,
            "location": obj.business.get_location,
            "verified": obj.business.is_verified
        }
        if (obj.business.media.logo.url):
            data["logo"] = request.build_absolute_uri(obj.business.media.logo.url)
        return data
    
    def get_user_marked_helpful(self, obj):
        request = self.context.get('request')
        user = request.user
        if (user.is_authenticated and obj.reactions.filter(user=user).exists()):
            return True
        else:
            return False

        
class ReviewHelpfulSerializer(serializers.ModelSerializer):
    class Meta:
        model = biz_model.ReviewHelpful
        fields = "__all__"
        
class BusinessMediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = biz_model.BusinessMedia
        fields = "__all__"

class BusinessHoursSerializers(serializers.ModelSerializer):
    class Meta:
        model = biz_model.BusinessHours
        fields = "__all__"
    
class BusinessContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = biz_model.BusinessContact
        fields = "__all__"