from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^get_chrild_type/$', views.get_chrild_type, name='get_chrild_type'),
    # url(r'^sitemap/$', views.sitemap, name='sitemap'),
    url(r'^load_articles/$', views.load_articles, name='load_articles'),
]