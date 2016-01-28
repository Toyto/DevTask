import json

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product


class ProductsView(ListView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 2
    context_object_name = 'products'


class SingleProductView(TemplateView):
    template_name = 'product/single_product.html'

    def get_context_data(self, **kwargs):
        context = super(SingleProductView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        context['single_product'] = product
        context['total_likes'] = product.total_likes
        return context


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        product = get_object_or_404(Product, slug=slug)

        if product.likes.filter(id=user.id).exists():
            product.likes.remove(user)
            message = 'You disliked this'
        else:
            product.likes.add(user)
            message = 'You liked this'

    context = {'likes_count': product.total_likes, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    