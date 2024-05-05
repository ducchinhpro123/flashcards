import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import TagForm, CardForm, DeckForm
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
            return redirect('flashcards_app:home')
        else:
            messages.error(request, "Invalid data entry.")
            return render(request, 'flashcards_app/add_card.html', context={"form": form})
    else:
        form = CardForm(request.POST or None, user=request.user)
        tag_form = TagForm()
        return render(request, 'flashcards_app/add_card.html', context={"form": form, "tag_form": tag_form})


def add_deck(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            messages.success(request, "Deck added successfully.")
            return redirect('flashcards_app:home')
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
    max_id = Card.objects.all().aggregate(max_id=Max("id"))['max_id']
    random_id = random.randint(1, max_id)

    next_card_one = Card.objects.filter(id=random_id, deck__user=request.user).first()

    while not next_card_one:
        random_id = random.randint(1, max_id)
        next_card_one = Card.objects.filter(id=random_id, deck__user=request.user).first()

    if next_card_one:
        return redirect('flashcards_app:memorize', card_id=next_card_one.id)
    else:
        return redirect('flashcards_app:home')


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
