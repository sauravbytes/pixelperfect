from django.urls import path
from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='Homepage'),
    path('services', views.ServiceView.as_view(), name='services'),
    path('image-upload', views.upload_image, name='image-upload'),
]
