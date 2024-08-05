from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404
from .models import Category, Subcategory,Product,Adresse, UserFavorite
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ProductForm,AdresseForm
# Create your views here.

def homepage(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    ville = request.GET.get('ville', '')

    # Filtre
    if search_query:
        products = products.filter(nom__icontains=search_query)
    if ville:
        products = products.filter(ville__icontains=ville)

    # Pagination
    paginator = Paginator(products, 2)  # 10 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'ville': ville,
    }
    return render(request, 'pro_commerce/home.html', context)
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
        'category':category,
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
        'products': products,
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
#
@login_required
def favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = UserFavorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})

    return JsonResponse({'status': 'added'})
#
@login_required
def favorite_list(request):
    favorite_products =UserFavorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'pro_commerce/favorite_liste.html', {'favorites': favorite_products})
#
def dashboard_user(request):
    return render(request,'Admin/admin.html')
#DASHBOARD PARTY...................................................................................
def annonce(request):
    return render(request,'Admin/pro_admin/annonce.html')
#--------------------------ADMIN PARTY---------------------------------
#----------------------------------------------------------------------
#PRODUCT

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.utilisateur = request.user
            product.save()
            messages.success(request, 'Le produit a été enregistré avec succès.')
            return redirect('dashboard')  # Redirigez vers une vue liste de produits ou autre
        else:
            messages.error(request, 'Erreur lors de l\'enregistrement du produit. Veuillez vérifier les informations.')
    else:
        form = ProductForm()
    
    return render(request, 'Admin/pro_admin/add_product.html', {'form': form})
#

 # Fetch products for the logged-in user
def product_admin(request):

    products = Product.objects.filter(utilisateur=request.user)
    # Fetch addresses for the logged-in user
    addresses = Adresse.objects.filter(utilisateur=request.user)
    
    # Pass both products and addresses to the template
    context = {
        'products': products,
        'addresses': addresses,
    }
    
    return render(request, 'Admin/admin.html', context)
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('product:list')
#     else:
#         form = ProductForm()
#     return render(request, 'product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('pro_commerce:dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'Admin/pro_admin/product_update.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('pro_commerce:dashboard')
    return render(request, 'Admin/admin.html', {'product': product})
#-----------------------------------------------------------
#ADRESSE
#----------------------------------------------------------

@login_required
def adresse_create(request):
    if request.method == 'POST':
        form = AdresseForm(request.POST)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.utilisateur = request.user
            adresse.save()
            return redirect('some_success_url')  # Redirect to a success page or list of addresses
    else:
        form = AdresseForm()
    
    context = {
        'form': form,
        'products': Product.objects.all(),  # Make sure to pass the products for the dropdown
    }
    return render(request, 'Admin/pro_admin/adresse_form.html', context)
#

@login_required
def user_addresses(request):
    # Fetch the addresses for the logged-in user
    addresses = Adresse.objects.filter(utilisateur=request.user)
    return render(request, 'user_addresses.html', {'addresses': addresses})
#
@login_required
def update_address(request, pk):
    address = get_object_or_404(Adresse, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        form = AdresseForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('pro_commerce:dashboard')
    else:
        form = AdresseForm(instance=address)
    return render(request, 'Admin/pro_admin/adresse_update.html', {'form': form})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Adresse, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('pro_commerce:dashboard')
    return render(request, 'confirm_delete.html', {'address': address})