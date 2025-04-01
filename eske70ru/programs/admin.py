from django.contrib import admin
from filebrowser.sites import site
from .models import *


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'languages', 'platforms', 'short_description', 'date', 'is_active']
    list_display_links = ['id', 'name', 'date']
    search_fields = ['name']
    list_editable = ('is_active',)


@admin.register(SoftDownload)
class SoftDownloadAdmin(admin.ModelAdmin):
    list_display = ['id', 'program_id', 'ip_remote', 'date', 'count']
    list_display_links = ['program_id']


# Register your models here.
admin.site.register(Languages)
admin.site.register(Platforms)
# admin.site.register(SoftDownload)