# Generated by Django 5.0.4 on 2024-05-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards_app', '0002_alter_tag_cards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='cards',
        ),
        migrations.AddField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='cards', to='flashcards_app.tag'),
        ),
    ]
