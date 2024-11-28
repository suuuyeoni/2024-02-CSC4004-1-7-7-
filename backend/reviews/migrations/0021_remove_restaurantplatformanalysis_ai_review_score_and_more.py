# Generated by Django 5.1.2 on 2024-11-24 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0020_rename_manual_label_attempted_review_manual_sentiment_label_attempted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurantplatformanalysis',
            name='ai_review_score',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='ai_review_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
