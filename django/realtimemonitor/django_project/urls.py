from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^clients/', views.clients),
    url(r'^$', TemplateView.as_view(template_name='dashboard.html')),
]
