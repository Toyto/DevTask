from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product

# Create your views here.
class ProductsView(TemplateView):
    template_name = 'product/products.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context