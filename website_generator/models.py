from django.db import models
from django.contrib.auth.models import User
import uuid

class GeneratedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_pages')
    industry = models.CharField(max_length=100)
    html_content = models.TextField()
    preview_url = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.industry} - {self.preview_url}"