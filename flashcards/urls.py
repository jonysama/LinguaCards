from django.urls import path
from . import views

urlpatterns = [
    # === API ПУТИ (Бэкенд для Postman) ===
    path('api/languages/', views.language_list, name='language-list'),
    path('api/contact/', views.submit_contact_form, name='contact-form'),
    path('api/decks/', views.DeckListCreateAPIView.as_view(), name='deck-list-create'),
    path('api/decks/<int:pk>/', views.DeckDetailAPIView.as_view(), name='deck-detail'),

    # === ФРОНТЕНД ПУТИ (Для браузера) ===
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-deck/', views.create_deck_view, name='create-deck'),
    path('deck/<int:deck_id>/add-card/', views.add_card_view, name='add-card'),
    path('deck/<int:deck_id>/', views.view_deck_cards, name='view-deck'),
]