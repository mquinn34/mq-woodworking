# admin.py
from django.contrib import admin
from .models import Product, ProductVariant

class ProductVariantInline(admin.TabularInline): 
    model = ProductVariant
    extra = 0  



class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

admin.site.register(Product, ProductAdmin,)

