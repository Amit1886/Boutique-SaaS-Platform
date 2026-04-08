from django.conf import settings
from django.db import models


class UserRole(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    VENDOR = "vendor", "Vendor"
    TAILOR = "tailor", "Tailor"
    ADMIN = "admin", "Admin"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    phone = models.CharField(max_length=30, blank=True)
    profile_img = models.ImageField(upload_to="profiles/", null=True, blank=True)
    language = models.CharField(max_length=5, default="en")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"

