from .models import Category

def categories_processor(request):
    categories=Category.objects.all().prefetch_related('souscategories')

    return {'categories': categories}
