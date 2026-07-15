from .models import Language

def global_stats(request):
    
    return {'total_languages': Language.objects.count()}