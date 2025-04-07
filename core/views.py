from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
import uuid
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ProcessedImage
from zeroscratches import EraseScratches
from PIL import Image
import PIL.Image
import time
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.core.files.storage import default_storage
from .models import PrivacyPolicy, AboutUs, HomePage, ServicePage, ImageCropper, ImageConverter, ImageResizer, UpscaleImage, ImageCompressor
from seo.models import SeoMeta
# Create your views here.


# @login_required()
def HomeView(request):
    content = get_object_or_404(HomePage)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }

    return render(request, 'index.html', obj)


def Service(request):
    content = get_object_or_404(ServicePage)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }
    return render(request, 'services/services.html', obj)


def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']

        # Define paths
        original_dir = os.path.join(settings.MEDIA_ROOT, 'original_images')
        processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_images')

        # Ensure directories exist
        os.makedirs(original_dir, exist_ok=True)
        os.makedirs(processed_dir, exist_ok=True)

        # Save uploaded image
        original_image_path = os.path.join(original_dir, uploaded_image.name)
        with open(original_image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        # Process the image
        image = Image.open(original_image_path).convert("RGB")
        eraser = EraseScratches()
        processed_img_array = eraser.erase(image)

        # Convert back to an image
        processed_img = Image.fromarray(processed_img_array)

        # Save processed image
        processed_image_name = f"processed_{uploaded_image.name}"
        processed_image_path = os.path.join(processed_dir, processed_image_name)
        processed_img.save(processed_image_path)

        # Save paths in the database
        processed_image = ProcessedImage.objects.create(
            original_image=f'original_images/{uploaded_image.name}',
            processed_image=f'processed_images/{processed_image_name}'
        )

        return redirect('image_result', image_id=processed_image.id)

    return render(request, 'index.html')


def image_result(request, image_id):
    image = ProcessedImage.objects.get(id=image_id)
    return render(request, 'result.html', {'image': image})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def ProfileLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {'username': username})  # or your desired view name
        else:
            error = "Invalid username or password"

            return render(request, 'registration/login.html', {"error": error})


def CropImage(request):
    content = get_object_or_404(ImageCropper)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }

    if request.method == 'POST':
        image_file = request.FILES.get('image')
        scale = float(request.POST.get('scale'))

        if image_file and scale:
            # Save uploaded image temporarily
            original_path = default_storage.save('temp/' + image_file.name, image_file)
            full_path = os.path.join(settings.MEDIA_ROOT, original_path)

            # Open the image
            img = Image.open(full_path)
            width, height = img.size

            # Calculate scaled crop box (center crop)
            new_w = int(width * scale)
            new_h = int(height * scale)
            left = (width - new_w) // 2
            top = (height - new_h) // 2
            right = left + new_w
            bottom = top + new_h

            cropped = img.crop((left, top, right, bottom))

            # Save cropped image
            cropped_filename = 'cropped_' + image_file.name
            cropped_path = os.path.join(settings.MEDIA_ROOT, 'cropped', cropped_filename)
            os.makedirs(os.path.dirname(cropped_path), exist_ok=True)
            cropped.save(cropped_path)

            cropped_url = settings.MEDIA_URL + 'cropped/' + cropped_filename
            return render(request, 'services/cropper/done.html', {'cropped_url': cropped_url})

    return render(request, 'services/cropper/scale_crop_form.html', obj)


def ResizeImage(request):
    content = get_object_or_404(ImageResizer)
    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }

    if request.method == 'POST':
        image_file = request.FILES.get('image')
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))

        if image_file and width and height:
            # Save original image temporarily
            original_path = default_storage.save('temp/' + image_file.name, image_file)
            full_original_path = os.path.join(settings.MEDIA_ROOT, original_path)

            # Open and resize
            img = Image.open(full_original_path)
            resized_img = img.resize((width, height))

            # Save resized image
            resized_filename = 'resized_' + image_file.name
            resized_path = os.path.join(settings.MEDIA_ROOT, 'resized', resized_filename)
            os.makedirs(os.path.dirname(resized_path), exist_ok=True)
            resized_img.save(resized_path)

            resized_url = settings.MEDIA_URL + 'resized/' + resized_filename
            return render(request, 'services/resizer/done.html', {'resized_url': resized_url})

    return render(request, 'services/resizer/resize_form.html', obj)


def CompressImage(request):
    content = get_object_or_404(ImageCompressor)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        quality = int(request.POST.get('quality'))

        if image_file and quality:
            # Save uploaded image temporarily
            original_path = default_storage.save('original/' + image_file.name, image_file)
            full_path = os.path.join(settings.MEDIA_ROOT, original_path)

            # Open image and compress
            img = Image.open(full_path)
            compressed_name = 'compressed_' + image_file.name
            compressed_path = os.path.join(settings.MEDIA_ROOT, 'compressed', compressed_name)

            os.makedirs(os.path.dirname(compressed_path), exist_ok=True)

            img.save(compressed_path, optimize=True, quality=quality)

            compressed_url = settings.MEDIA_URL + 'compressed/' + compressed_name
            return render(request, 'services/compressor/compressed_done.html', {'compressed_url': compressed_url})

    return render(request, 'services/compressor/compress_form.html', obj)


def ConvertImage(request):
    content = get_object_or_404(ImageConverter)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        target_format = request.POST.get('format')  # e.g., JPEG, PNG, etc.

        if uploaded_file and target_format:
            # Save uploaded file temporarily
            original_path = default_storage.save('original/' + uploaded_file.name, uploaded_file)
            full_path = os.path.join(settings.MEDIA_ROOT, original_path)

            # Open and convert image
            img = Image.open(full_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")  # Avoid issues with JPEG

            # Set new name and format
            base_name = os.path.splitext(uploaded_file.name)[0]
            new_file_name = f"{base_name}_converted.{target_format.lower()}"
            output_path = os.path.join(settings.MEDIA_ROOT, 'converted', new_file_name)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, format=target_format.upper())

            converted_url = settings.MEDIA_URL + 'converted/' + new_file_name
            return render(request, 'services/converter/converted_done.html', {'converted_url': converted_url})

    return render(request, 'services/converter/convert_form.html', obj)


def ImageUpscale(request):
    content = get_object_or_404(UpscaleImage)

    seo_meta = SeoMeta(
        title=content.title,
        seo_title=content.seo_title,
        description=content.meta_description,
        keywords=content.keywords,
        canonical_url=request.build_absolute_uri(request.path)
    )

    obj = {
        'seo_meta': seo_meta
    }

    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        width = request.POST.get('width')
        height = request.POST.get('height')

        if uploaded_file and width and height:
            try:
                width = int(width)
                height = int(height)

                # Save original image
                original_path = default_storage.save('originals/' + uploaded_file.name, uploaded_file)
                full_path = os.path.join(settings.MEDIA_ROOT, original_path)

                # Open and resize
                img = Image.open(full_path)
                resized_img = img.resize((width, height), Image.LANCZOS)

                # Save resized image
                base_name, ext = os.path.splitext(uploaded_file.name)
                new_name = f"{base_name}_{width}x{height}{ext}"
                resized_path = os.path.join(settings.MEDIA_ROOT, 'resized', new_name)
                os.makedirs(os.path.dirname(resized_path), exist_ok=True)

                resized_img.save(resized_path)

                result_url = settings.MEDIA_URL + 'resized/' + new_name
                return render(request, 'services/upscale/resize_result.html', {'url': result_url, 'width': width, 'height': height})

            except Exception as e:
                return render(request, 'services/upscale/resize_form.html', {'error': str(e)})

    return render(request, 'services/upscale/resize_form.html', obj)


def privacy(request):
    obj = {
        'content': PrivacyPolicy.objects.all()
    }

    return render(request, 'privacy-policy.html', obj)


def about(request):
    obj = {
        'content': AboutUs.objects.all()
    }

    return render(request, 'about-us.html', obj)