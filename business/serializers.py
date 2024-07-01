from rest_framework import serializers
import business.models as biz_model 

class BusinessCategoriesSerializers(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = biz_model.BusinessCategory
        fields = '__all__'
        debth = 2
        

class BusinessReviewSerializer(serializers.ModelSerializer):
    # business_logo = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    business = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = biz_model.BusinessReview
        fields = ["id", "rating", "title", "review", "created_at", "updated_at", "business", "helpful_count", "user"]
        
    def get_business(self, obj):
        request = self.context.get('request')
        data = {
            "reviews_number": obj.business.reviews_count,
            "name": obj.business.name,
            "location": obj.business.get_location,
            "verified": obj.business.is_verified
        }
        if (obj.business.media.logo.url):
            data["logo"] = request.build_absolute_uri(obj.business.media.logo.url)
        return data
        
class ReviewHelpfulSerializer(serializers.ModelSerializer):
    class Meta:
        model = biz_model.ReviewHelpful
        fields = "__all__"
        
class BusinessMediaSerializers(serializers.ModelSerializer):
    class Meta:
        model = biz_model.BusinessMedia
        fields = "__all__"