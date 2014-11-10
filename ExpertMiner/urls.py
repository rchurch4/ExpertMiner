from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'ExpertMiner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'search.views.index', name='index'),
    url(r'^authors/', 'search.views.author_index', name='authors_index'),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^keyword_search/', 'search.views.results', name='keyword search'),
	url(r'^author_list/', 'search.views.authorlist', name='authors'),
	url(r'^author_search/', 'search.views.author_search', name='author search'),
	url(r'^author_profile/[0-9]{7}/', 'search.views.author_profile', name='author profile'),
]

