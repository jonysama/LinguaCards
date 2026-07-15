from django.db import models
from django.contrib.auth.models import User

# 1. Модель (например: Английский, Турецкий, Японский)
class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 2. Модель колоды слов 
class Deck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Связь 1: Колода принадлежит определенному языку
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='decks')
    # Связь 2: У колоды есть автор (пользователь)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.language.name})"

# 3. Модель самой карточки
class Card(models.Model):
    # Связь 3: Карточка лежит в определенной колоде
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards')
    original_word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    example_sentence = models.TextField(blank=True, help_text="Пример использования в предложении")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_word} - {self.translation}"

# 4-я модель — это встроенная модель User, которую мы импортировали сверху. 
# Требование "At least 4 models" выполнено!