import random
import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import TagForm, CardForm, DeckForm, DeckAndTagsForm, CardFormTest, CsvForm
from .models import *


# Create your views here.

def home(request):
    user = request.user
    if user.is_authenticated:
        decks = Deck.objects.filter(user=user)
        decks_count = decks.count()
    else:
        decks = []
        decks_count = 0
    return render(request, 'flashcards_app/home.html',
                  context={"decks": decks, "decks_count": decks_count})


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('flashcards_app:login')
    template_name = 'flashcards_app/register.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Invalid data entry.')
        return response


def login_form(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flashcards_app:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'flashcards_app/login.html')


def logout_now(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect("flashcards_app:home")


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        next_url = request.POST.get('next', '/')
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            messages.success(request, "Tag added successfully.")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/add_tag.html', context={"form": form})
    else:
        form = TagForm()
        return render(request, 'flashcards_app/add_tag.html', context={"form": form})


def add_card(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Card added successfully.")
            # Delete this session, if a new card is added, it'll fetch again
            if 'card_ids' in request.session:
                del request.session['card_ids']
            return redirect('flashcards_app:home')
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/add_card.html', context={"form": form})
    else:
        form = CardForm(request.POST or None, user=request.user)
        tag_form = TagForm()
        deck_form = DeckForm()
        return render(request, 'flashcards_app/add_card.html',
                      context={"form": form, "tag_form": tag_form, "deck_form": deck_form})


def add_multiple_cards(request):
    extra_number = request.GET.get('extra_number')
    if extra_number is None:
        extra_number = 1  # default value for number of form
    CardFormSet = formset_factory(CardFormTest, extra=int(extra_number))
    if request.method == "POST":
        deck_and_tags_form = DeckAndTagsForm(request.POST, user=request.user)
        formset = CardFormSet(request.POST)
        if deck_and_tags_form.is_valid() and formset.is_valid():
            deck = deck_and_tags_form.cleaned_data['deck']
            tags = deck_and_tags_form.cleaned_data['tags']
            for form in formset:
                card = form.save(commit=False)
                card.deck = deck
                card.save()
                card.tags.set(tags)
            messages.success(request, "Cards added successfully.")
            if 'card_ids' in request.session:
                del request.session['card_ids']
            return redirect('flashcards_app:home')
        else:
            messages.error(request, "Invalid data entry.")
    else:
        deck_and_tags_form = DeckAndTagsForm(user=request.user)
        formset = CardFormSet()
    return render(request, 'flashcards_app/add_multiple_cards.html',
                  context={"formset": formset, "deck_and_tags_form": deck_and_tags_form})


def add_deck(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        next_url = request.POST.get('next', '/')

        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            messages.success(request, "Deck added successfully.")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/add_deck.html', context={"form": form})
    else:
        form = DeckForm()
        return render(request, 'flashcards_app/add_deck.html', context={"form": form})


def deck_detail(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    cards = Card.objects.filter(deck=deck)
    return render(request, 'flashcards_app/view_deck.html', context={"deck": deck, "cards": cards})


def cards_view(request):
    cards = []
    if request.method == "POST":
        tag_name = request.POST.get('tag_name')
        cards = Card.objects.filter(deck__user=request.user, tags__name=tag_name)

    tags = Tag.objects.filter(user=request.user)
    return render(request, 'flashcards_app/cards_view.html', context={"tags": tags, "cards": cards})


def next_card(request):
    if 'card_ids' in request.session:
        card_ids = request.session['card_ids']
    else:
        card_ids = list(Card.objects.filter(deck__user=request.user).values_list('id', flat=True))
        request.session['card_ids'] = card_ids

    if not card_ids:
        return redirect('flashcards_app:home')
    random_id = random.choice(card_ids)

    try:
        next_card_one = Card.objects.get(id=random_id)
    except ObjectDoesNotExist:
        if 'card_ids' in request.session:
            del request.session['card_ids']
        return redirect('flashcards_app:cards')

    return redirect('flashcards_app:memorize', card_id=next_card_one.id)


def card_detail(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render(request, 'flashcards_app/card_detail.html', context={'card': card})


def update_card(request, card_id):
    card = Card.objects.get(pk=card_id)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, "Card updated successfully.")
            return redirect('flashcards_app:deck-detail', card.deck.id)
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/update_card.html', context={"form": form})
    else:
        form = CardForm(instance=card)
        return render(request, 'flashcards_app/update_card.html', context={"form": form})


def tags_view(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'flashcards_app/tags_view.html', context={"tags": tags})


def change_password(request):
    user = request.user
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'flashcards_app/change_password.html')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully.")
            return redirect('flashcards_app:home')
        else:
            messages.error(request, "Invalid old password.")
    return render(request, 'flashcards_app/change_password.html')


def delete_card(request, card_id):
    try:
        card = Card.objects.get(pk=card_id)
        card.delete()
        if 'card_ids' in request.session:
            del request.session['card_ids']
    except ObjectDoesNotExist:
        messages.error(request, "Not found.")
    return redirect("flashcards_app:cards")


def update_tag(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    if tag is None:
        messages.error(request, "Tag not found.")
        return redirect('flashcards_app:tags')
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag updated successfully.")
            return redirect('flashcards_app:tags')
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/update_tag.html', context={"form": form})
    else:
        form = TagForm(instance=tag)
        return render(request, 'flashcards_app/update_tag.html', context={"form": form})


def upload_csv(request):
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            cards = read_cards_from_csv(csv_file)
            user = request.user
            for card_data in cards:
                try:
                    deck = Deck.objects.get(id=card_data['deck_id'], user=user)
                except Deck.DoesNotExist:
                    continue
                card = Card.objects.create(question=card_data['question'], answer=card_data['answer'], deck=deck)
                cards = card_data['tags']

                for tag_name in cards:
                    tag, created = Tag.objects.get_or_create(name=tag_name, user=user)
                    card.tags.add(tag)
                card.save()
            card_ids = list(Card.objects.filter(deck__user=request.user).values_list('id', flat=True))
            request.session['card_ids'] = card_ids
            return redirect('flashcards_app:home')
    else:
        form = CsvForm()
    return render(request, 'flashcards_app/upload_csv.html',
                  {'form': form})


def read_cards_from_csv(file):
    cards = []

    file_data = file.read().decode('utf-8').splitlines()
    reader = csv.reader(file_data)
    next(reader)  # Skip header row
    for row in reader:
        card = {
            'question': row[0],
            'answer': row[1],
            'deck_id': row[2],  # assume the deck existed, otherwise: except Deck.DoesNotExist: continue
            'tags': row[3].split(';') if row[3] else [],

        }
        cards.append(card)
    return cards
