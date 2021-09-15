# Generated by Django 3.2.7 on 2021-09-15 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Файл', upload_to='files')),
                ('name', models.CharField(help_text='Имя файла', max_length=255)),
                ('file_type', models.CharField(choices=[('i', 'image'), ('m', 'music'), ('v', 'video'), ('d', 'document'), ('p', 'presentation'), ('t', 'table')], help_text='Тип файла', max_length=1)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('public', models.BooleanField(default=False, help_text='Доступен для неавторизованных пользователей')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]