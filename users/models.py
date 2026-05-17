from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
     # Role choices
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('compounder', 'Compounder'),
        ('receptionist', 'Receptionist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # record creation timestamp
    updated_at = models.DateTimeField(auto_now=True)      # record last update

    def __str__(self):
        return f"{self.username} ({self.role})"

