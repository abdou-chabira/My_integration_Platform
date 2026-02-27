from django.urls import path
from .views import WebhookView, OAuthConnectView, MonitoringView

urlpatterns = [
    path("webhook/", WebhookView.as_view()),
    path("oauth/connect/", OAuthConnectView.as_view()),
    path("monitoring/", MonitoringView.as_view()),
]