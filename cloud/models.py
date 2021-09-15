from django.contrib.auth import get_user_model
from django.db import models


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
    slug = models.SlugField(unique=True, null=True)
    public = models.BooleanField(help_text='Доступен для неавторизованных пользователей', default=False)
