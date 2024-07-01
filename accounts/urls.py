from django.urls import path, include
import accounts.views as accounts_views 
import business.views as business_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pa/profile', accounts_views.PersonalProfileAccountViewSet, basename='profile')
# router.register('pa/review', accounts_views.ReviewViewSet, basename='review')



urlpatterns = [
    path('signup/', accounts_views.PersonalSignupView.as_view(), name='personal_signup'),
    path('signup/business', accounts_views.BusinessSignupView.as_view(), name='business_signup'),
    path('users/me/', accounts_views.UserMeView.as_view()),
    path('', include('authemail.urls')),
    
] + router.urls