from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import PersonalLocation, PersonalSocial
from authemail.admin import EmailUserAdmin

class MyUserAdmin(EmailUserAdmin):
    readonly_fields = ['date_joined']
    fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal Info', {'fields': ('first_name', 'last_name')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions', 'is_business', 'is_personal')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), MyUserAdmin)

admin.site.register(PersonalLocation)
admin.site.register(PersonalSocial)