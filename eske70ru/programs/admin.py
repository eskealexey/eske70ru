from django.contrib import admin
from .models import *

from django.contrib import admin
# from tinymce.widgets import TinyMCE
from django.db import models

#
# class ProgramAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': TinyMCE()},
#     }


# Register your models here.
admin.site.register(Languages)
# admin.site.register(Program, ProgramAdmin)
admin.site.register(Program)
admin.site.register(Platforms)