from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'channels/$',
        views.ChannelList.as_view(),
        name='channel-list'),
    url(r'channels/(?P<channel_name>(\w|-)+)/$',
        views.ChannelDetail.as_view(),
        name='channel-detail'),
    url(r'channels/(?P<channel_name>(\w|-)+)/(?P<category_name>(\w|-)+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail')
]
