from django.db import models
from django.core.exceptions import ValidationError


class Quote(models.Model):
    source = models.CharField(max_length=255)
    text = models.TextField()
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.source}: {self.text[:50]}"
