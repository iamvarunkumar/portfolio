from django.db import models

from django.db import models
import uuid # Optional: If you want a unique ID per download/visit record

class WebsiteVisit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    # Add other fields you might derive or want to store

    def __str__(self):
        return f"{self.ip_address} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp'] # Show newest visits first in admin


class ResumeDownload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField()
    download_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    # user_email = models.EmailField(null=True, blank=True) # Only if you have a way to capture it

    def __str__(self):
        return f"Resume downloaded by {self.ip_address} at {self.download_time}"

    class Meta:
        ordering = ['-download_time']

# --- Remember to run migrations ---
# python manage.py makemigrations portfolio
# python manage.py migrate
