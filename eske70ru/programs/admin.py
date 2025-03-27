from django.contrib import admin
from filebrowser.sites import site
from .models import *


# Register your models here.
admin.site.register(Languages)
admin.site.register(Program)
admin.site.register(Platforms)
admin.site.register(SoftDownload)