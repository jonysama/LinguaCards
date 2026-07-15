from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Deck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='decks')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.language.name})"


class Card(models.Model):
    
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    original_word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    example_sentence = models.TextField(blank=True, help_text="Пример использования в предложении")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_word} - {self.translation}"

