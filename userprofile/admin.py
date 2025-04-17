from django.contrib import admin

# Register your models here.

from .models import UserProfile, WorkExperience, Education, Portfolio

admin.site.register(UserProfile)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(Portfolio)