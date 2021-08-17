from django.db import models
from django.db.models.deletion import CASCADE


class Reaction(models.Model):
    """Create instances of the Tag class"""
    label = models.CharField(max_length=50)
    image_url = models.TextField()

