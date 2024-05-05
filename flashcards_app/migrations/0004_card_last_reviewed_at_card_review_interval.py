# Generated by Django 5.0.4 on 2024-05-05 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards_app', '0003_remove_tag_cards_card_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='last_reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='review_interval',
            field=models.IntegerField(default=1),
        ),
    ]
