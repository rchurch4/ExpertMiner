# search/urls.py

from django.conf.urls import patterns, url
from search import views

# urls

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^results/', views.results, name='results'),
	url(r'^authors/', views.authorlist, name='authors'),
)