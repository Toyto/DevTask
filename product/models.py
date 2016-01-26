from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(blank=False, unique=True)
    description = models.CharField(max_length=300, default='None')
    price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    likes = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name