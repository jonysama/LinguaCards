from .models import Language

def global_stats(request):
    # Возвращает словарь, который будет доступен в любом HTML-шаблоне
    return {'total_languages': Language.objects.count()}