from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','title','category', 'status', 'views')
    list_display_links = ('id', 'title')
    list_editable = ('status',)


# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'author', 'parent', 'text','is_active', 'created_at')
    list_display_links = ('id', 'project','author', 'parent', 'text')
    list_editable = ('is_active',)



# admin.site.register(Project)
admin.site.register(Comment, CommentAdmin)
