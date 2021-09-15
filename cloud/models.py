from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class File(models.Model):
    file = models.FileField(upload_to='files', help_text='Файл')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    name = models.CharField(max_length=255, help_text='Имя файла')
    FILE_TYPES = (
        ('i', 'image'),
        ('m', 'music'),
        ('v', 'video'),
        ('d', 'document'),
        ('p', 'presentation'),
        ('t', 'table'),
    )
    file_type = models.CharField(max_length=1, choices=FILE_TYPES, help_text='Тип файла')
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    public = models.BooleanField('Публичный файл', help_text='Доступен для неавторизованных пользователей',
                                 default=False)

    @property
    def icon_url(self):
        return settings.MEDIA_URL + 'file_icons/' + self.file_type + '.png'
