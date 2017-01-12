from django.conf.urls import include, url
from django.contrib import admin
from django_app.views import clients
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', clients, name='clients'),
    url(r'^$', TemplateView.as_view(template_name='dashboard.html')),
]
