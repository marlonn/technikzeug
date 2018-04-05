
from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'artikel'
urlpatterns = [
    url(r'^$', views.SearchView.as_view(), name="search"),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^api/$', views.ArtikelList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ArtikelDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

