# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('barangay_official', 'Barangay Official'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.username