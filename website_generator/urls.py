from django.urls import path
from .views import WebsiteGenerationView, WebsiteListView, WebsiteDetailView

urlpatterns = [
    path('generate/', WebsiteGenerationView.as_view(), name='website-generate'),
    path('list/', WebsiteListView.as_view(), name='website-list'),
    path('<str:website_id>/', WebsiteDetailView.as_view(), name='website-detail'),
]