from django.contrib import admin
from .models import Product, Comment

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'modified_at']
    list_filter = ('likes',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'posted_at']


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)