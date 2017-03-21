from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search_data, name='index'),
    url(r'^results/(?P<item>.+)/(?P<typedata>.+)$', views.results, name='results'),
]