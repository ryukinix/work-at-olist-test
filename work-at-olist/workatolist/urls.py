from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = [
    url('^$', lambda request: redirect('core:channel-list')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('core.urls', namespace='core'))
]
