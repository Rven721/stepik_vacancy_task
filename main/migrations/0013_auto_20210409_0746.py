# Generated by Django 3.0.4 on 2021-04-09 07:46

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210408_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
