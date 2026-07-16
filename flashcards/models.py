from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    # Stores available languages for learning, for example English, Kazakh, Spanish.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Deck(models.Model):
    # Deck is a collection of flashcards created by a specific user.
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Each deck belongs to one language.
    # related_name='decks' allows us to get all decks for a language.
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='decks'
    )

    # Each deck is connected to the authenticated user who created it.
    # If the user is deleted, all his/her decks will also be deleted.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='decks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.language.name})"


class Card(models.Model):
    # Card stores one word, its translation, and an optional example sentence.

    # Each card belongs to one deck.
    # If the deck is deleted, all related cards will also be deleted.
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name='cards'
    )

    original_word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    example_sentence = models.TextField(
        blank=True,
        help_text="Пример использования в предложении"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_word} - {self.translation}"
