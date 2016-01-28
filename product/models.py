from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(blank=False, unique=True)
    description = models.CharField(max_length=300, default='None')
    price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes')

    def __unicode__(self):
        return self.name

    @property
    def total_likes(self):
        """
        Likes for the product
        :return: Integer: Likes for the product
        """
        return self.likes.count()


class Comment(models.Model):
    product = models.ForeignKey(Product)
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

