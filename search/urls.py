# search/urls.py

from django.conf.urls import patterns, url
from search import views

# urls

urlpatterns = patterns('',
	url(r'^$', views.index, name="index"),
)