from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request,'pro_commerce/flex.html')
#
def detail(request):
    return render(request,'pro_commerce/detail.html')
#
def contacts(request):
    return render(request,'pro_commerce/contact.html')
#
def about(request):
    return render(request,'pro_commerce/apropos.html')