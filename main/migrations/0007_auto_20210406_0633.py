# Generated by Django 3.0.4 on 2021-04-06 06:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210403_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='written_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='https://place-hold.it/100x60', upload_to='company_images'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(default='https://place-hold.it/100x60', upload_to='speciality_images'),
        ),
    ]
