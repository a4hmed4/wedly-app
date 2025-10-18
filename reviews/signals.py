# reviews/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from halls.models import Hall
from django.db import models

@receiver(post_save, sender=Review)
def update_hall_rating_on_save(sender, instance, created, **kwargs):
    hall = instance.hall
    agg = hall.reviews.aggregate(avg=models.Avg('rating'), cnt=models.Count('id'))
    hall.average_rating = agg['avg'] or None
    hall.reviews_count = agg['cnt'] or 0
    hall.save(update_fields=['average_rating', 'reviews_count'])


@receiver(post_delete, sender=Review)
def update_hall_rating_on_delete(sender, instance, **kwargs):
    hall = instance.hall
    agg = hall.reviews.aggregate(avg=models.Avg('rating'), cnt=models.Count('id'))
    hall.average_rating = agg['avg'] or None
    hall.reviews_count = agg['cnt'] or 0
    hall.save(update_fields=['average_rating', 'reviews_count'])
