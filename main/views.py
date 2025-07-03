from collections import defaultdict
from contextlib import nullcontext

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from product.models import (Category, Subcategory, Product,
                            ProductImage, SubcategoryFilters, SubcategoryFiltersValues, ProductFilters,GroupProductFilters)
from django.db.models import Count, Q
import ast


# Create your views here.
def index(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/index.html', {'categories': categories})

def contact(request):
    categories = Category.objects.prefetch_related('subcategories')
    return render(request, 'main/contact.html', {'categories': categories})
#Finished here

def singleProductByFilter(request, productUrl, productFilter):
    categories = Category.objects.prefetch_related('subcategories')
    product = (Product.objects.prefetch_related('images').
               filter(url=productUrl).order_by('images__is_main'))
    productFilters = (ProductFilters.objects.filter(product_id=product.first().id).
                      order_by('subcategoryFilters_id'))

    productFiltersNew = defaultdict(list)

    groupByValue = 0
    index = 0
    # Here I group All properties and settings of the product
    for productFilter in productFilters:
        if productFilter == productFilters[0]:
            productFiltersNew[groupByValue].append(productFilter)
        elif productFilter.subcategoryFilters.name == productFilters[index-1].subcategoryFilters.name:
            # Here we delete duplicates
            existing_values = [pf.subcategoryFiltersValues for pf in productFiltersNew[groupByValue]]
            if productFilter.subcategoryFiltersValues not in existing_values:
                productFiltersNew[groupByValue].append(productFilter)
        else:
            groupByValue += 1
            productFiltersNew[groupByValue].append(productFilter)
        index += 1

    productFiltersNew = dict(productFiltersNew)
    #print(productFiltersNew[0][1].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFilters.name)
    return render(request, 'main/detail.html', {'categories': categories,
                                                'product': product, 'productFilters': productFiltersNew})


def singleProduct(request, productUrl):
    categories = Category.objects.prefetch_related('subcategories')
    product = (Product.objects.prefetch_related('images').
               filter(url=productUrl).order_by('images__is_main'))
    productFilters = (ProductFilters.objects.filter(product_id=product.first().id).
                      order_by('subcategoryFilters_id'))

    productFiltersNew = defaultdict(list)

    groupByValue = 0
    index = 0
    # Here I group All properties and settings of the product
    for productFilter in productFilters:
        if productFilter == productFilters[0]:
            productFiltersNew[groupByValue].append(productFilter)
        elif productFilter.subcategoryFilters.name == productFilters[index-1].subcategoryFilters.name:
            # Here we delete duplicates
            existing_values = [pf.subcategoryFiltersValues for pf in productFiltersNew[groupByValue]]
            if productFilter.subcategoryFiltersValues not in existing_values:
                productFiltersNew[groupByValue].append(productFilter)
        else:
            groupByValue += 1
            productFiltersNew[groupByValue].append(productFilter)
        index += 1

    productFiltersNew = dict(productFiltersNew)
    #print(productFiltersNew[0][1].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFiltersValues.name)
    # print(productFilters[0].subcategoryFilters.name)
    return render(request, 'main/detail.html', {'categories': categories,
                                                'product': product, 'productFilters': productFiltersNew})

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

#Here I get products price etc. but you need to send
# properties and settings(Color: red, Size: X, etc.)
def getProductByPropsAndSettings(request):
    required_SubCategoryFiltersId = ast.literal_eval(request.GET.get('properties'))
    required_SubCategoryFiltersValuesId = ast.literal_eval(request.GET.get('settings'))
    productId=2
    required_SubCategoryFiltersIdCount=len(required_SubCategoryFiltersId)

    #matching_groups=ProductFilters.objects.filter(product_id=productId).values('groupProductFilters_id','id','subcategoryFilters_id','subcategoryFiltersValues_id')
    matching_groups=(ProductFilters.objects.
                     filter(subcategoryFilters_id__in=required_SubCategoryFiltersId, subcategoryFiltersValues_id__in=required_SubCategoryFiltersValuesId,
                            product_id=productId).
                     values('groupProductFilters_id').
                     annotate(count=Count('subcategoryFilters_id', distinct=True)).
                     filter(count=required_SubCategoryFiltersIdCount))[:1]

    if(matching_groups):
        groupProductFiltersId=matching_groups[0]['groupProductFilters_id']
        print("________________")
        print(groupProductFiltersId)


        priceOfProduct=GroupProductFilters.objects.filter(id=groupProductFiltersId).values("price")[0]['price']

        print("________________")
        print(priceOfProduct)

    required_SubCategoryFiltersId = ast.literal_eval(request.GET.get('properties'))
    print(required_SubCategoryFiltersId)
    return JsonResponse(priceOfProduct,safe=False)
