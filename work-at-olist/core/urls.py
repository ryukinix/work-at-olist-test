from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'channels/$',
        views.ChannelList.as_view(),
        name='channels'),
    url(r'channels/(?P<channel_name>(\w|-)+)/$',
        views.ChannelDetail.as_view(),
        name='channels_categories'),
    url(r'channels/(?P<channel_name>(\w|-)+)/(?P<category_name>(\w|-)+)/$',
        views.ChannelCategory.as_view(),
        name='channels_category')
]
