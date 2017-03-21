from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_tree, name='tree'),
    url(r'^alignment$', views.get_alignment, name='alignment'),
]