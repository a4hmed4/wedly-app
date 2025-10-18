from django.db import models
from django.conf import settings
from halls.models import Hall

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hall')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.hall.name} ({self.rating})"
