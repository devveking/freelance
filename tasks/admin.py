
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'budget', 'status', 'created_at')
    list_filter = ('status', 'category', 'tags')
    search_fields = ('title', 'description')

