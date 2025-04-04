from django.urls import path
from core import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='Homepage'),
    path('services', views.ServiceView.as_view(), name='services'),
    path('image-upload', views.process_image, name='image-upload'),
    path('result/<int:image_id>/', views.image_result, name='image_result'),
]
