from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', 'django_app.views.clients'),
    url(r'^$', TemplateView.as_view(template_name='dashboard.html')),
)
