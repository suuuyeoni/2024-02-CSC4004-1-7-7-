# Generated by Django 5.1.2 on 2024-11-26 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0021_remove_restaurantplatformanalysis_ai_review_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewExtra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('selected_menu', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'reviews_extra',
            },
        ),
    ]
