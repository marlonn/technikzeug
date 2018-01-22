
from django.conf.urls import url
from . import views

app_name = 'artikel'
urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^suche$', views.SearchView.as_view(), name="search"),
    url(r'^$', views.SearchView.as_view(), name="search"),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
