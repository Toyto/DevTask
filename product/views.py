from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Product


# Create your views here.
class ProductsView(ListView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 2
    context_object_name = 'products'


class SingleProductView(TemplateView):
    template_name = 'product/single_product.html'

    def get_context_data(self, **kwargs):
        context = super(SingleProductView, self).get_context_data(**kwargs)
        context['single_product'] = get_object_or_404(Product, slug=self.kwargs['slug'])
        return context