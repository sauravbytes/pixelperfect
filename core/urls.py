from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core import views

urlpatterns = [
    path('', views.HomeView, name='homepage'),
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("profile/", views.ProfileLogin, name="profile-login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('services/', views.Service, name='services'),
    path('image-upload/', views.process_image, name='image-upload'),
    path('result/<int:image_id>/', views.image_result, name='image_result'),
    path('image-cropper/', views.CropImage, name='image-cropper'),
    path('image-resizer/', views.ResizeImage, name='image-resizer'),
    path('image-compressor/', views.ImageCompressor, name='image-compressor'),
    path('image-converter/', views.ConvertImage, name='image-converter'),
    path('image-upscale/', views.ImageUpscale, name='image-upscale'),
    path('about-us', views.about, name='about-us'),
    path('privacy-policy', views.privacy, name='privacy-policy'),
    path('our-ai-model', views.AImodels, name='ai-model'),
    path('cnn-upload-image', views.CNNupload, name='cnn-upload-image'),
    path('gan-upload-image', views.GANupload, name='gan-upload-image'),
    path('cnn-image', views.cnn_image, name='cnn-image'),
    path('gan-image', views.gan_image, name='gan-image')

]
