from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView
from mysite.views import BasicArithmeticForm
from mysite.models import Level, Worksheet

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name='index.html'), name='mysite_home'),
    url(r'^(?i)about', TemplateView.as_view(template_name='about.html')),
    url(r'^(?i)contact', 'mysite.views.contact', name='contact.html'),
    url(r'^(?i)thankyou', TemplateView.as_view(template_name='contact_thankyou.html')),
	url(r'^(?i)addition/$', TemplateView.as_view(template_name='addition/index.html')),
	#url(r'^(?i)addition/basic',  'mysite.views.basicAddition' ),
    url(r'^(?i)worksheets',
        ListView.as_view(
            queryset=Worksheet.objects.all().order_by('worksheet_name', 'level'),
            context_object_name='worksheet_list',
            template_name='worksheets.html')),
	#url(r'^(?i)addition/some_view',  'mysite.views.some_view' ),
    #url(r'^(?i)addition/generatePDF/(?P<rows>\d+)/(?P<cols>\d+)/$',  'mysite.views.generatePDF', name='generatePDF' ),
    url(r'^(?i)addition/generatePDFWorksheet/(?P<worksheet_id>\d+)/$',  'mysite.views.generatePDFWorksheet', name='generatePDFWorksheet' ),

    url(r'^register/', 'mysite.views.register', name='mysite_register'),
    url(r'^login_test/', 'mysite.views.login_test', name='mysite_login_test'),
)
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/', 'login', {'template_name': 'login.html'}, name='mysite_login'),
    url(r'^logout/', 'logout', {'next_page': '/login'}, name='mysite_logout'),

)
