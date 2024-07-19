# api/models.py
from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to='documents/')
    improved_content = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
