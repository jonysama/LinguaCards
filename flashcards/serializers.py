from rest_framework import serializers
from .models import Language, Deck, Card



class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class DeckSerializer(serializers.ModelSerializer):
    
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Deck
        fields = ['id', 'title', 'description', 'language', 'author', 'created_at']




class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()

class WordCheckSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=255)
    user_translation = serializers.CharField(max_length=255)