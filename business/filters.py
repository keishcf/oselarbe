from django_filters import rest_framework as filters
from business.models import BusinessReview

class BusinessReviewFilterSet(filters.FilterSet):
    class Meta:
        model = BusinessReview
        fields = ['rating', 'created_at']