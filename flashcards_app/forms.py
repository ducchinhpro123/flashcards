from django import forms

from flashcards_app.models import Tag, Card, Deck


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class CardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['answer'].required = False
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
            self.fields['deck'].queryset = Deck.objects.filter(user=user)

    class Meta:
        model = Card
        fields = ['deck', 'tags', 'question', 'answer']


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'description']
