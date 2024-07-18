from django.shortcuts import get_object_or_404, render,get_list_or_404
from .models import Category, Subcategory,Product,Adresse

# Create your views here.
def homepage(request):
    #
    products=Product.objects.all()
    search_query= request.GET.get('search','')
    ville= request.GET.get('ville','')
    #filtre
    if search_query:
        products= products.filter(nom__icontains=search_query)
        print(products)
    if ville:
        products=products.filter(ville__icontains=ville)
        
    context={
        'products':products,
        'search_query':search_query,
        'ville':ville
    }
    return render(request,'pro_commerce/home.html',context)
#
def all_products(request):
    products=Product.objects.all()
    return render(request,'pro_commerce/all_product.html',
                  {
                      'products':products
                  })

def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    ville= request.GET.get('ville','')

    # category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(categorie=category)
    if ville:
        products=products.filter(ville__icontains=ville)
     
    context={
        # 'category':category,
        'products':products,
        'category':category
    }
    return render(request, 'pro_commerce/product_categorie.html', context)


def products_by_subcategory(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
    products = Product.objects.filter(sous_categorie=subcategory)
    ville= request.GET.get('ville','')
    if ville:
        products=products.filter(ville__icontains=ville)
  

    context = {
        'subcategory': subcategory,
        'products': products
    }
    return render(request, 'pro_commerce/product_sous-categorie.html', context)
# #

def detail(request, product_id):
    # Récupérer le produit spécifique par son ID
    product = get_object_or_404(Product, id=product_id)
    adresse_vendeur= Adresse.objects.filter(produit=product_id)
    
    # Récupérer les produits similaires de la même catégorie, en excluant le produit actuel
    similar_products = Product.objects.filter(categorie=product.categorie).exclude(id=product_id)
    #
    categories=Category.objects.all().prefetch_related('souscategories')

    #

    context = {
        'product': product,               # Passer le produit au contexte du template
        'similar_products': similar_products,
        'adresse_vendeur':adresse_vendeur,
                              'categories': categories,

    }
    return render(request, 'pro_commerce/detail.html', context)

def contacts(request):
    return render(request,'pro_commerce/contact.html')
#
def about(request):
    return render(request,'pro_commerce/apropos.html')
#

def custom_404_view(request, exception):
    return render(request, '404.html', {}, status=404)