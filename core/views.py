from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import View

# Create your views here.


class HomeView(View):

    def get(self, request):
        return render(request, 'index.html')

