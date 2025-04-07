from django.contrib import admin
from core.models import (ProcessedImage, PrivacyPolicy, AboutUs, HomePage, ServicePage, ImageCropper, ImageResizer,
                         ImageConverter, ImageCompressor, UpscaleImage)
# Register your models here.


admin.site.register(ProcessedImage),
admin.site.register(PrivacyPolicy),
admin.site.register(AboutUs),
admin.site.register(HomePage),
admin.site.register(ServicePage),
admin.site.register(ImageCropper),
admin.site.register(ImageResizer),
admin.site.register(ImageConverter),
admin.site.register(ImageCompressor),
admin.site.register(UpscaleImage),
