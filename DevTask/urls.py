from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView

from product.views import ProductsView, SingleProductView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DevTask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^products/$', ProductsView.as_view(), name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', SingleProductView.as_view(), name='single_product'),
    url(r'^$', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/products'
    )),
    url(r'^logout/$',
        'django.contrib.auth.views.logout', name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/products')),
)
