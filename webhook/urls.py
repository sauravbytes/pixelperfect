from django.urls import path
from .views import GitHubWebhookView

urlpatterns = [
    path('webhook/', GitHubWebhookView.as_view(), name='github-webhook')
]
