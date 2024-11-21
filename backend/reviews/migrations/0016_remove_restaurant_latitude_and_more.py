# Generated by Django 5.1.2 on 2024-11-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_remove_restaurantplatforminfo_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='longitude',
        ),
        migrations.AddField(
            model_name='restaurantplatforminfo',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurantplatforminfo',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
