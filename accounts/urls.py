from django.urls import path, include
import accounts.views as accounts_views 
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('signup/', accounts_views.PersonalSignupView.as_view(), name='personal_signup'),
    path('signup/business', accounts_views.BusinessSignupView.as_view(), name='business_signup'),
    path('users/me/', accounts_views.UserMeView.as_view()),
    path('', include('authemail.urls')),
    path('pa/profile', accounts_views.ProfileRetriveUpdateDestroy.as_view(), name="profile_list_create"),
    path('pa/profile/<pk>', accounts_views.ProfileDetail.as_view()),
    path('pa/p/location', accounts_views.PersonalLocationCreateView.as_view()),
    path('pa/p/location/<pk>', accounts_views.PersonalLocationRetrieveEditDestroy.as_view()),
    path('pa/p/social', accounts_views.PSocialMediaListCreate.as_view()),
    path('pa/p/social/<pk>', accounts_views.PSocialMediaRetriveUpdateDestroy.as_view()),
]