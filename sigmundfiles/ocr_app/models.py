from django.db import models
from django.utils import timezone

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)  # Valor predeterminado
    wordcloud = models.ImageField(upload_to='wordclouds/', null=True, blank=True)

    def __str__(self):
        return self.image.name
