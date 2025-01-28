# my_app/models.py
from django.db import models

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='uploads/', blank=True, null=True)
    image = models.ImageField(upload_to='job_images/', null=True, blank=True)  # Allows job posts without images
    def __str__(self):
        return self.title
