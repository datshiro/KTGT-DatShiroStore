# Generated by Django 2.0.5 on 2018-05-12 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DatShiroShop', '0005_auto_20180508_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='extension',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
