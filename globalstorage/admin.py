from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.FileExtension)
class FileExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'size_limit', 'description')