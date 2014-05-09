from django.conf.urls.defaults import *

urlpatterns = patterns('zookeeper_dashboard.zkadmin.views',
    (r'^server/(?P<server_id>\d+)/$','detail'), 
    (r'^server/delete$','serverDelete'), 
    (r'^$','index'), 
    (r'^idle/$','idle'), 
    (r'^idle/delete$', 'idleDelete'),
    (r'^idle/deploy/$', 'idleDeploy'),
)
