from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$',
        TemplateView.as_view(template_name='index.html')),
)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/', 'login', {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/', 'logout', {'next_page': '/login'}, name='mysite_logout'),
)