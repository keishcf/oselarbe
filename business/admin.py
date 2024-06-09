from django.contrib import admin
from accounts.models import PersonalProfile
from business.models import BusinessCategory, BusinessProfile
# Register your models here.


admin.site.register(BusinessProfile)
admin.site.register(PersonalProfile)
admin.site.register(BusinessCategory)



