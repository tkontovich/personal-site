from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    dates = models.CharField(max_length=150)
    description = models.TextField()
