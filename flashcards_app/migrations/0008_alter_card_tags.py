# Generated by Django 5.0.4 on 2024-06-20 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards_app', '0007_alter_card_created_at_alter_card_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='cards', to='flashcards_app.tag'),
        ),
    ]