from django.contrib import admin

from cloud.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'file', 'name', 'file_type', 'public')
