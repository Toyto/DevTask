import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, FormView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product, Comment
from .forms import CommentForm


class IndexView(TemplateView):
    template_name = 'base.html'


class ProductsView(ListView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 2
    context_object_name = 'products'


class SingleProductView(FormView):
    template_name = 'product/single_product.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(SingleProductView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        context['single_product'] = product
        context['total_likes'] = product.total_likes
        context['comments'] = Comment.objects.filter(
            product=product).order_by('-posted_at')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            text = form.cleaned_data.get('text')
            slug = request.POST.get('product_slug')
            product = Product.objects.get(slug=slug)
            Comment.objects.create(product=product, text=text)
            return redirect('single_product', slug)

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
