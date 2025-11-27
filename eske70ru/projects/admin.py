from django.contrib import admin

from .models import *

# # Register your models here.
# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('id','title','category', 'status', 'views')
#     list_display_links = ('id', 'title')
#     list_editable = ('status',)


# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'author', 'parent', 'text','is_active', 'created_at')
    list_display_links = ('id', 'project','author', 'parent', 'text')
    list_editable = ('is_active',)


# admin.site.register(Project)
admin.site.register(Comment, CommentAdmin)


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'file_type', 'get_file_size_display', 'download_count', 'uploaded_at']
    list_filter = ['file_type', 'is_active', 'uploaded_at']
    search_fields = ['name', 'description', 'project__title']
    readonly_fields = ['size', 'download_count', 'uploaded_at']
    list_select_related = ['project']

    def get_file_size_display(self, obj):
        return obj.get_file_size_display()

    get_file_size_display.short_description = 'Размер'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    readonly_fields = ['size', 'download_count', 'uploaded_at']
    fields = ['file', 'name', 'file_type', 'description', 'size', 'download_count', 'is_active']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # ... существующие настройки ...
    inlines = [ProjectFileInline]
    list_display = ['title', 'author', 'category', 'status', 'files_count', 'rating', 'views']