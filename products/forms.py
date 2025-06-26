from django import forms
from ckeditor.widgets import CKEditorWidget
from products.models import Product, ProductVariant
from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
   
    class Meta:
        model = Product
        fields = ['name', 'description', 'slug', 'product_type', 'is_featured', 'image']
        widgets = {'description': forms.Textarea(attrs={'rows': 5}),}


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['wood_type', 'size', 'price_modifier']

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    extra=1,
    can_delete=True
)