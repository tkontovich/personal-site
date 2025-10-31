from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    dates = models.CharField(max_length=150)
    description = models.TextField()
    
    # Sortable field (for django-admin-sortable2)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.title} at {self.company}"