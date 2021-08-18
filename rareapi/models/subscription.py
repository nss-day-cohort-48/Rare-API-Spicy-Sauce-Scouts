from django.db import models
from django.db.models.deletion import CASCADE


class Subscription(models.Model):
    """Create instances of the Tag class"""
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="author")
    created_on = models.DateField()
    ended_on = models.DateField(null=True)

