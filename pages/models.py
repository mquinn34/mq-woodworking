from django.db import models
from cloudinary.models import CloudinaryField

class GalleryImage(models.Model):
    image = CloudinaryField('image', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
