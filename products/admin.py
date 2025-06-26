# admin.py
from django.contrib import admin
from .models import Product, ProductVariant

class ProductVariantInline(admin.TabularInline):  # or StackedInline
    model = ProductVariant
    extra = 0  # how many empty forms to show

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]

admin.site.register(Product, ProductAdmin)

