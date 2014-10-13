# search/urls.py

from django.conf.urls import patterns, url
from search import views

# urls

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
	#url(r'^author_index/', views.author_index, name ='author index'),
)