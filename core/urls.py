from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core import views

urlpatterns = [
    path('', views.HomeView, name='homepage'),
    path("accounts/", include("django.contrib.auth.urls"), name="login"),
    path("profile/", views.ProfileLogin, name="profile-login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('services', views.ServiceView, name='services'),
    path('image-upload', views.process_image, name='image-upload'),
    path('result/<int:image_id>/', views.image_result, name='image_result'),
]
