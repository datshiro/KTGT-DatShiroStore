# Generated by Django 2.0.5 on 2018-05-15 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatShiroShop', '0009_profile_drive_folder_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Song Name'),
        ),
    ]
