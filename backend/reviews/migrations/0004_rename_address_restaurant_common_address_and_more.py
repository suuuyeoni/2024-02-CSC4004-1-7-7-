# Generated by Django 5.1.2 on 2024-11-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_restaurant_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='address',
            new_name='common_address',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='detail_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
