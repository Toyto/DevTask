from django.conf.urls import include, url, patterns
from django.contrib import admin
from product.views import ProductsView, SingleProductView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DevTask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^products/$', ProductsView.as_view(), name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', SingleProductView.as_view(), name='single_product'),
)
