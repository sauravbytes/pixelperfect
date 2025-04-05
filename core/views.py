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
# Create your views here.


# @login_required()
def HomeView(request):

    return render(request, 'index.html')


def ServiceView(request):
    return render(request, 'services.html')


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

    return render(request, 'upload.html')


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

