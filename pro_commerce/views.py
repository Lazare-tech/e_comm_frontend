from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404
from .models import Category, ReviewRating, Subcategory,Product,Adresse, UserFavorite
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ProductForm,AdresseForm, ReviewForm
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
    
    # Récupérer les produits similaires de la même catégorie, en excluant le produit actuel
    similar_products = Product.objects.filter(categorie=product.categorie).exclude(id=product_id)
    #
    categories=Category.objects.all().prefetch_related('souscategories')

    #

    context = {
        'product': product,               # Passer le produit au contexte du template
        'similar_products': similar_products,
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
        form = ProductForm(request.POST, request.FILES,user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.utilisateur = request.user
            product.save()
            messages.success(request, 'Le produit a été enregistré avec succès.')
            return redirect('pro_commerce:dashboard')  # Redirigez vers une vue liste de produits ou autre
        else:
            messages.error(request, 'Erreur lors de l\'enregistrement du produit. Veuillez vérifier les informations.')
    else:
        form = ProductForm(user=request.user)
    
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
    
        return render(request,'Admin/admin.html',context)

#UPDATE PRODUCT


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if form.is_valid():
            # Sauvegarde du produit, y compris la photo si un nouveau fichier est téléchargé
            form.save()
            messages.success(request, 'Le produit a été mis à jour avec succès.')
            return redirect('pro_commerce:dashboard')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ProductForm(instance=product, user=request.user)

    return render(request, 'Admin/pro_admin/product_update.html', {'form': form})
#DELETE PRODUCT
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Le produit a été supprimé avec succès.')

        return redirect('pro_commerce:dashboard')
    
    # Optionally, you can render a confirmation page here if not using a modal
    return redirect('pro_commerce:dashboard')

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
            messages.success(request, 'L\'adresse a été mis à jour avec succès.')

            return redirect('pro_commerce:dashboard')  # Redirect to a success page or list of addresses
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
            messages.success(request, 'L\'adresse a été mis à jour avec succès.')

            return redirect('pro_commerce:dashboard')
    else:
        form = AdresseForm(instance=address)
    return render(request, 'Admin/pro_admin/adresse_update.html', {'form': form})

@login_required
def delete_address(request, pk):
    address = get_object_or_404(Adresse, pk=pk, utilisateur=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'L\adresse a été supprime avec succès.')

        return redirect('pro_commerce:dashboard')
    return render(request, 'confirm_delete.html', {'address': address})
#

@login_required
def rate(request, product_id: int, rating: int):
    product = get_object_or_404(Product, id=product_id)
    review, created = ReviewRating.objects.update_or_create(
        produit=product,
        user=request.user,
        defaults={'rating': rating}
    )
    if not created:
        review.save()  # Save the review if it was updated
    return redirect('pro_commerce:product_detail', product_id=product_id)

def rate(request, service_id: int, rating: int) -> HttpResponse:
    post = Product.objects.get(id=service_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return render(request,'pro_commerce/base.html')
#
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, produit__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.produit_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
# def rate(request, product_id: int, rating: int) -> HttpResponse:
#     post = Product.objects.get(id=product_id)
#     Rating.objects.filter(post=post, user=request.user).delete()
#     post.rating_set.create(user=request.user, rating=rating)
#     return render(request,'pro_commerce/base.html')
# # #
# def submit_review(request, services_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = ReviewRating.objects.get(user__id=request.user.id, service__id=services_id)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, 'Thank you! Your review has been updated.')
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.service_id = services_id
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, 'Thank you! Your review has been submitted.')
#                  return redirect(url)