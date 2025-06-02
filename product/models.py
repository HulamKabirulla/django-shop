from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',)
    url = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL,null=True,
    blank=True,
    default=None)
    url = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    url = models.CharField(max_length=100, default="")
    is_main = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class SubcategoryFilters(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

class SubcategoryFiltersValues(models.Model):
    name = models.CharField(max_length=100)
    subcategoryFilters = models.ForeignKey(SubcategoryFilters, on_delete=models.CASCADE, related_name='subcategoryFiltersValues')

class GroupProductFilters(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    is_available = models.BooleanField(default=True)

class ProductFilters(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subcategoryFilters = models.ForeignKey(SubcategoryFilters, on_delete=models.CASCADE)
    subcategoryFiltersValues = models.ForeignKey(SubcategoryFiltersValues, on_delete=models.CASCADE)
    groupProductFilters = models.ForeignKey(GroupProductFilters, on_delete=models.CASCADE)