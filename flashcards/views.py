from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, DeckForm, CardForm
from .models import Language, Deck
from .serializers import (
    LanguageSerializer, DeckSerializer, ContactFormSerializer
)

# требование FBV (Функции)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def language_list(request):
    if request.method == 'GET':
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_form(request):
    serializer = ContactFormSerializer(data=request.data)
    if serializer.is_valid():
        return Response({"message": "Form submitted successfully!"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# требование CBV (Классы) + Полный CRUD + request.user

class DeckListCreateAPIView(APIView):
    # Требуем, чтобы пользователь был залогинен
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Чтение (Read): Пользователь видит только свои колоды
        decks = Deck.objects.filter(author=request.user)
        serializer = DeckSerializer(decks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Создание (Create)
        serializer = DeckSerializer(data=request.data)
        if serializer.is_valid():
            # КРИТИЧЕСКОЕ ТРЕБОВАНИЕ: Привязка к request.user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Deck, pk=pk, author=user)

    def get(self, request, pk):
        # Чтение одной конкретной колоды (Read)
        deck = self.get_object(pk, request.user)
        serializer = DeckSerializer(deck)
        return Response(serializer.data)

    def put(self, request, pk):
        # Обновление (Update)
        deck = self.get_object(pk, request.user)
        serializer = DeckSerializer(deck, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Удаление (Delete)
        deck = self.get_object(pk, request.user)
        deck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, DeckForm

# ==========================================
# FRONTEND VIEWS (Отображение в браузере)
# ==========================================

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Требование: Handle errors gracefully (Успешное сообщение)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            # Требование: Handle errors gracefully (Сообщение об ошибке)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'flashcards/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'flashcards/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

def home_view(request):
    # Выводим все колоды на главной странице
    decks = Deck.objects.all().order_by('-created_at')
    return render(request, 'flashcards/home.html', {'decks': decks})

@login_required(login_url='login')
def create_deck_view(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.author = request.user
            deck.save()
            messages.success(request, 'Deck created successfully!')
            return redirect('home')
    else:
        form = DeckForm()
    return render(request, 'flashcards/create_deck.html', {'form': form})

@login_required(login_url='login')
def add_card_view(request, deck_id):
    # Находим колоду, в которую хотим добавить карточку
    from django.shortcuts import get_object_or_404
    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck # Привязываем карточку к этой колоде
            card.save()
            messages.success(request, f'Card successfully added to "{deck.title}"!')
            return redirect('home')
    else:
        form = CardForm()

    return render(request, 'flashcards/add_card.html', {'form': form, 'deck': deck})

def view_deck_cards(request, deck_id):
    from django.shortcuts import get_object_or_404
    # Находим нужную колоду
    deck = get_object_or_404(Deck, id=deck_id)

    # Достаем все карточки, связанные с этой колодой 
    # (мы использовали related_name='cards' в моделях)
    cards = deck.cards.all().order_by('-created_at')

    return render(request, 'flashcards/deck_detail.html', {'deck': deck, 'cards': cards})