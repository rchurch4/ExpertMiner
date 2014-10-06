# search/urls.py

from django.conf.urls import patterns, url
from search import views

# urls

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	url(r'^keyword_search/', views.results, name='keyword search'),
	url(r'^author_list/', views.authorlist, name='authors'),
	url(r'^author_search/', views.author_search, name='author search'),
	#url(r'^author_index/', views.author_index, name ='author index'),
)