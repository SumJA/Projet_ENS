from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search_data, name='index'),
    url(r'^results/(?P<item>.+)/(?P<typedata>.+)$', views.results, name='results'),
    url(r'^Tree/(?P<item>.+)/(?P<typedata>.+)$', views.Tree, name='Tree'),
    url(r'^Align/(?P<item>.+)/(?P<typedata>.+)$', views.Align, name='Align'),
    url(r'^All/(?P<item>.+)/(?P<typedata>.+)$', views.All, name='All'),
    url(r'^Expr/(?P<item>.+)/(?P<typedata>.+)$', views.Expr, name='Expr'),

]
