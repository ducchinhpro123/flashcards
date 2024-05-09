from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name="flashcards_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("add-tag/", views.add_tag, name="add-tag"),
    path("add-card/", views.add_card, name="add-card"),
    path("add-deck/", views.add_deck, name="add-deck"),
    path("login/", views.login_form, name="login"),
    path("logout/", views.logout_now, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

    path("deck/<int:deck_id>/", views.deck_detail, name="deck-detail"),
    path("cards/", views.cards_view, name="cards"),
    path("tags/", views.tags_view, name="tags"),
    path("next-card/", views.next_card, name="next-card"),
    path("memorize/<int:card_id>/", views.card_detail, name="memorize"),

    path("update-card/<int:card_id>/", views.update_card, name="update-card"),
    path("delete-card/<int:card_id>/", views.delete_card, name="delete-card"),
    path("update-tag/<int:tag_id>/", views.update_tag, name="update-tag"),
    path("add-multiple-cards/", views.add_multiple_cards, name="add-multiple-cards"),

]
