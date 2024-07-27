from django.contrib import admin
from accounts.models import PersonalProfile
import business.models as biz_models
# Register your models here.


admin.site.register(biz_models.BusinessProfile)
admin.site.register(PersonalProfile)
admin.site.register(biz_models.BusinessCategory)
admin.site.register(biz_models.BusinessReview)
admin.site.register(biz_models.ReviewHelpful)
admin.site.register(biz_models.BusinessQuestions)
admin.site.register(biz_models.BusinessMedia)
admin.site.register(biz_models.BusinessContact)



