from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'company', 'dates']
    search_fields = ['title', 'company']