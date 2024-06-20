from django.contrib import admin
from .models import *


# Register your models here.

class InlineTag(admin.TabularInline):
    model = Tag.cards.through


class CardAdmin(admin.ModelAdmin):
    list_display = ['question', 'deck', 'created_at']
    list_filter = ['deck', 'tags']
    search_fields = ['question', 'answer']
    # inlines = [InlineTag]


class DeckAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Card, CardAdmin)
admin.site.register(Tag)
admin.site.register(Deck, DeckAdmin)
