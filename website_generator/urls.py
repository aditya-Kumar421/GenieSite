from django.urls import path
from .views import GeneratePageView, PreviewPageView, EditPageView, ListPagesView

urlpatterns = [
    path('generate/', GeneratePageView.as_view(), name='generate_page'),
    path('preview/<str:preview_url>/', PreviewPageView.as_view(), name='preview_page'),
    path('edit/<str:preview_url>/', EditPageView.as_view(), name='edit_page'),
    path('list/', ListPagesView.as_view(), name='list_pages'),
]