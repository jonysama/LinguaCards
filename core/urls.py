from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Вот здесь мы убрали 'api/', чтобы главная страница открывалась по умолчанию!
    path('', include('flashcards.urls')), 
    
    path('api/login/', obtain_auth_token, name='api_token_auth'), 
]