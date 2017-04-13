from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'channels/$',
        views.ChannelList.as_view(),
        name='channels'),
    url(r'channels/(?P<channel_name>[a-z]+)/$',
        views.ChannelDetail.as_view(),
        name='channels_categories'),
    url(r'channels/(?P<channel_name>[a-z]+)/(?P<category_name>[a-z]+)/$',
        views.ChannelCategory.as_view(),
        name='channels_category')
]
