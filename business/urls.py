from django.urls import path
from .views import BusinessViewSet, ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('review', ReviewViewSet, basename='review')
router.register('biz', BusinessViewSet, basename='biz')

urlpatterns = [
   
] + router.urls
