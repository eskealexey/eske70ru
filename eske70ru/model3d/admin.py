from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
   list_display = ['id','title', 'category', 'format', 'status', 'created_at', 'download_count']
   list_editable = ['category', 'format', 'status']


admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Model3D)
admin.site.register(ModelImage)