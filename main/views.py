from django.http import HttpResponse
from django.shortcuts import render
from product.models import (Category, Subcategory, Product,
                            ProductImage, SubcategoryFilters, SubcategoryFiltersValues, ProductFilters)


# Create your views here.
def index(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/index.html', {'categories': categories})

def contact(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/contact.html', {'categories': categories})
#Finished here
def singleProduct(request, productUrl):
    categories = Category.objects.prefetch_related('subcategories')
    product = (Product.objects.prefetch_related('images').
               filter(url=productUrl).order_by('images__is_main'))
    productFilters = ProductFilters.objects.get(product_id=product.first().id)
    print(productFilters.subcategoryFiltersValues.name)
    return render(request, 'main/detail.html', {'categories': categories,
                                                'product': product})

def productsbycategory(request, category):
    categories = Category.objects.prefetch_related('subcategories')
    products = (Product.objects.select_related('category').prefetch_related('images').
                filter(category__url=category,images__is_main=True))[:12]

    return render(request, 'main/shop.html', {'categories': categories, 'products': products})

def productsbysubcategory(request, category,subcategory):
    categories = Category.objects.prefetch_related('subcategories')
    #products = (Product.objects.select_related('category').select_related('subcategory').prefetch_related('images').
                #filter(category__url=category,subcategory__url=subcategory, images__is_main=True))[:12]

    currentCategory = Category.objects.get(url=category)
    currentSubCategory = Subcategory.objects.get(url=subcategory)
    products = (Product.objects.prefetch_related('images').
                filter(category=currentCategory.id,subcategory=currentSubCategory.id, images__is_main=True))[:12]
    subcategoryFilters=(SubcategoryFilters.objects.
                        prefetch_related('subcategoryFiltersValues').
                        filter(subcategory=currentSubCategory))
    return render(request, 'main/shop.html', {'categories': categories, 'products': products, 'filters': subcategoryFilters})