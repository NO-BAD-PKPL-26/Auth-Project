from django.conf import settings
from django.db import models


class UserPreference(models.Model):
    FONT_CHOICES = [
        ("inria-serif", "Inria Serif"),
        ("inter", "Inter"),
        ("roboto", "Roboto"),
        ("plus-jakarta", "Plus Jakarta Sans"),
        ("petrona", "Petrona"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preference"
    )
    dark_mode = models.BooleanField(default=False)
    font = models.CharField(max_length=30, choices=FONT_CHOICES, default="inria-serif")

    def __str__(self):
        return f"{self.user.email} preference"