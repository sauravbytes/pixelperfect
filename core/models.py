from django.db import models
from tinymce.models import HTMLField
# Create your models here.
from seo.models import BaseMetaData
from django.db import models


class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class PrivacyPolicy(models.Model):
    content = HTMLField(help_text='Privacy Policy Content')


class AboutUs(models.Model):
    content = HTMLField(help_text='About Us Content')


class HomePage(BaseMetaData):
    content = HTMLField(help_text='home page content', null=True, blank=True)


class ServicePage(BaseMetaData):
    content = HTMLField(help_text='Service page content', null=True, blank=True)


class ImageCropper(BaseMetaData):
    content = HTMLField(help_text='Imaage Cropper page content', null=True, blank=True)


class ImageResizer(BaseMetaData):
    content = HTMLField(help_text='Image Resizer page content', null=True, blank=True)


class ImageCompressor(BaseMetaData):
    content = HTMLField(help_text='Image Compressor page content', null=True, blank=True)


class ImageConverter(BaseMetaData):
    content = HTMLField(help_text='Image Converter page content', null=True, blank=True)


class UpscaleImage(BaseMetaData):
    content = HTMLField(help_text='Upscale Image page content', null=True, blank=True)