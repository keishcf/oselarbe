from django.urls import path
from .views import ListBusinessCategory

urlpatterns = [
    path('categories/', ListBusinessCategory.as_view(), name="category_list")
]
