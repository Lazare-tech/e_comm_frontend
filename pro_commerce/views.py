from django.shortcuts import render
from .models import Category, Subcategory

# Create your views here.
def homepage(request):
    categories=Category.objects.all().prefetch_related('souscategories')

    return render(request,'pro_commerce/home.html',{'categories': categories})
#
def detail(request):
    return render(request,'pro_commerce/detail.html')
#
def contacts(request):
    return render(request,'pro_commerce/contact.html')
#
def about(request):
    return render(request,'pro_commerce/apropos.html')