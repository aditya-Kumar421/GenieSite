from django.urls import path
from .views import (
    WebsiteGenerationView, 
    WebsiteListView, 
    WebsiteDetailView,
    GeneratePreviewView,
    PreviewWebsiteView
)

urlpatterns = [
    path('generate/', WebsiteGenerationView.as_view(), name='website-generate'),
    path('list/', WebsiteListView.as_view(), name='website-list'),
    path('<str:website_id>/', WebsiteDetailView.as_view(), name='website-detail'),
    path('<str:website_id>/preview/', GeneratePreviewView.as_view(), name='generate-preview'),
    path('preview/<str:url_token>/', PreviewWebsiteView.as_view(), name='preview-website'),
]