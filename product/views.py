import json
import datetime

from django.views.generic import TemplateView, ListView, FormView
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Product, Comment
from .forms import CommentForm


class IndexView(TemplateView):
    template_name = 'base.html'


class ProductsView(ListView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 2
    context_object_name = 'products'

    def get_queryset(self):
        queryset = sorted(Product.objects.all(), key=lambda x: x.total_likes, reverse=True)
        return queryset


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
            messages.success(request, 'Thank for comment.')
            return redirect('single_product', slug)
        else:
            return HttpResponseBadRequest()


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        product = get_object_or_404(Product, slug=slug)
        if product.likes.filter(id=user.id).exists():
            product.likes.remove(user)
            messages.success(request, 'You disliked it.')
        else:
            product.likes.add(user)
            messages.success(request, 'You liked it.')

    context = {'likes_count': product.total_likes}
    return HttpResponse(json.dumps(context), content_type='application/json')
