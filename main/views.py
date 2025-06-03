from collections import defaultdict
from contextlib import nullcontext

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
    productFilters = ProductFilters.objects.filter(product_id=product.first().id).order_by('subcategoryFilters_id')

    productFiltersNew = defaultdict(list)

    groupByValue = 0
    index = 0
    for productFilter in productFilters:
        if productFilter == productFilters[0]:
            productFiltersNew[groupByValue].append(productFilter)
        elif productFilter.subcategoryFilters.name == productFilters[index-1].subcategoryFilters.name:
            productFiltersNew[groupByValue].append(productFilter)
        else:
            groupByValue += 1
            productFiltersNew[groupByValue].append(productFilter)
        index += 1
    print(productFiltersNew[0][1].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFilters.name)
    return render(request, 'main/detail.html', {'categories': categories,
                                                'product': product, 'productFilters': dict(productFiltersNew)})

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