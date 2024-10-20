from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('Answer', config_name='extends')
    deck = models.ForeignKey('Deck', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='cards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    review_interval = models.IntegerField(default=1, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.question


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Deck(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
