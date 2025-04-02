from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import ImageUpload

# Create your views here.


class HomeView(View):

    def get(self, request):
        return render(request, 'index.html')

class ServiceView(View):

    def get(self, request):
        return render(request, 'services.html')


def upload_image(request):
    if request.method == "POST":
        if "image" not in request.FILES:
            return HttpResponseBadRequest("No image uploaded.")

        image = request.FILES["image"]
        ImageUpload.objects.create(image=image)
        return HttpResponse("Image uploaded successfully!")

    return render(request, "index.html")


