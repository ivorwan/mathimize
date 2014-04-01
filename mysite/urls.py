from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from mysite.views import BasicArithmeticForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name='index.html')),
	url(r'^(?i)addition/$', TemplateView.as_view(template_name='addition/index.html')),
	url(r'^(?i)addition/basic',  'mysite.views.basicAddition' ),
	#url(r'^(?i)addition/some_view',  'mysite.views.some_view' ),
    url(r'^(?i)addition/generatePDF/(?P<rows>\d+)/(?P<cols>\d+)/$',  'mysite.views.generatePDF', name='generatePDF' ),
    url(r'^(?i)addition/generatePDFWorksheet/(?P<level>\w+)/$',  'mysite.views.generatePDFWorksheet', name='generatePDFWorksheet' ),
		
)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/', 'login', {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/', 'logout', {'next_page': '/login'}, name='mysite_logout'),
)