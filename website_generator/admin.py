from django.contrib import admin
from website_generator.models import GeneratedPage

@admin.register(GeneratedPage)
class GeneratedPageAdmin(admin.ModelAdmin):
    list_display = ('user', 'industry', 'preview_url', 'created_at', 'updated_at')
    search_fields = ('industry', 'preview_url')
    list_filter = ('created_at', 'updated_at')
# Register your models here.
