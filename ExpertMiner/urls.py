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
]

