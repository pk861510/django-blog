# Generated by Django 4.2.6 on 2024-03-09 11:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_rename_post_pst'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pst',
            new_name='post',
        ),
    ]
