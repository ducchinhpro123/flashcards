# Generated by Django 5.0.4 on 2024-05-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards_app', '0005_tag_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='review_interval',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]