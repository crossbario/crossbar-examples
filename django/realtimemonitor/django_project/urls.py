from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django_app import views as v

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', v.clients),
    url(r'^$', TemplateView.as_view(template_name='dashboard.html')),
]
