from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField



class Product(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField(unique = True)
    description = RichTextField()
    product_type = models.CharField(max_length = 100, default= 'None', choices=[
        ('record_cabinet', 'Record Cabinet'),
        ('dining_table', 'Dining Table'),
        ('coffee_table', 'Coffee Table')
    ])
    is_featured = models.BooleanField(default=False)
    main_image = CloudinaryField('image', blank=True)


    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    wood_type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price_modifier = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.wood_type} / {self.size} (+${self.price_modifier})"


    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name= 'images', on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True)
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.product.name} Image"
