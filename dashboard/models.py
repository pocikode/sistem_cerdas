from django.db import models


class Sentiment(models.Model):
    label = models.CharField(max_length=50)
    total = models.IntegerField(default=0)
