from django.conf.urls import patterns, url


urlpatterns = patterns(
    'searchcomparedemo.views',
    url(r'^weixin/', 'happy'),
    url(r'^dianping/', 'search'),
    url(r'^$','welcome'),
    url(r'^shopdemo/', 'shopsearch')

)
