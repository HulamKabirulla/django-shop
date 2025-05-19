from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('<str:category>/', views.productsbycategory),
    path('<str:category>/<str:subcategory>/', views.productsbysubcategory),
]