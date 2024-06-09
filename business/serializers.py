from rest_framework import serializers
from .models import BusinessCategory

class BusinessCategoriesSerializers(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = BusinessCategory
        fields = '__all__'
        debth = 2