# Generated by Django 4.2.6 on 2024-03-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_pst_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='prince',
            field=models.CharField(default='Prince', max_length=20),
            preserve_default=False,
        ),
    ]