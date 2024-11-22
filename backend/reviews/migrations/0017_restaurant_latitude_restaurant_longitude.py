# Generated by Django 5.1.2 on 2024-11-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_remove_restaurant_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
