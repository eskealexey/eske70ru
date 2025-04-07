from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Model3D)
admin.site.register(ModelImage)