from django.http import HttpResponse
from django.shortcuts import render
from product.models import Category, Product, ProductImage


# Create your views here.
def index(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/index.html', {'categories': categories})

def contact(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/contact.html', {'categories': categories})

def productsbycategory(request, category):
    categories = Category.objects.prefetch_related('subcategories')
    products = (Product.objects.select_related('category').prefetch_related('images').
                filter(category__url=category,images__is_main=True))

    return render(request, 'main/shop.html', {'categories': categories, 'products': products})

def productsbysubcategory(request, category,subcategory):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/shop.html', {'categories': categories})