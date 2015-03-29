from django.conf.urls import patterns, include, url

import server_status
from server_status.views import ServerStatusDashboard

server_status.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ServerStatusDashboard.as_view(), name='server-status-dashboard'),
)
