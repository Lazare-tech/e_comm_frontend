from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product,UserFavorite
from django.contrib.auth.decorators import login_required

def categories_processor(request):
    categories=Category.objects.all().prefetch_related('souscategories')

    return {'categories': categories}
#
def favorite_processor(request):
    
    if request.user.is_authenticated:
        favorite_products = UserFavorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        favorite_products=[]
    return{'favorite_products':favorite_products}
#
