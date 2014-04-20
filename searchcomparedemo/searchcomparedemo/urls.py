from django.conf.urls import patterns, url


urlpatterns = patterns(
    'searchcomparedemo.views',
    url(r'^$', 'search'),
)
