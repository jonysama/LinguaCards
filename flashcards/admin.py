from django.contrib import admin
from .models import Language, Deck, Card

#admin
admin.site.register(Language)
admin.site.register(Deck)
admin.site.register(Card)