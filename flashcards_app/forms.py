from django import forms
from django.forms import formset_factory

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


class DeckAndTagsForm(forms.Form):
    deck = forms.ModelChoiceField(queryset=Deck.objects.none())
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['deck'].queryset = Deck.objects.filter(user=user)
            self.fields['tags'].queryset = Tag.objects.filter(user=user)


class CardFormTest(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['answer'].required = False

    class Meta:
        model = Card
        fields = ['question', 'answer']




class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'description']
