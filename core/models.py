from django.db import models

# Create your models here.

from django.db import models


class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

