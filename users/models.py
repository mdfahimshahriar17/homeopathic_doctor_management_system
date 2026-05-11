from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('doctor', 'Doctor'),
        ('compounder', 'Compounder'),
        ('admin', 'Admin'),
    ]

    #Adding role field
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)

    #Optional: Additional field
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    # __str__ method
    def __str__(self):
        return f"{self.username} ({self.role})"
