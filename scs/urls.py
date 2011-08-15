"""scs.urls"""

from __future__ import absolute_import

from django.contrib import admin
from django.conf.urls.defaults import (patterns, include, url,  # noqa
                                       handler500, handler404)

from piston.resource import Resource

from . import api
from . import views

admin.autodiscover()


class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)


node_resource = CsrfExemptResource(handler=api.NodeHandler)
queue_resource = CsrfExemptResource(handler=api.QueueHandler)


urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^node/create/', views.create_node),
    (r'^node/(?P<nodename>[^/]+)/enable', views.enable_node),
    (r'^node/(?P<nodename>[^/]+)/disable', views.disable_node),
    (r'^node/(?P<nodename>[^/]+)/restart', views.restart_node),
    (r'^node/(?P<nodename>[^/]+)/delete', views.delete_node),
    (r'^api/node/(?P<nodename>[^/]+)/', node_resource),
    (r'^api/node/', node_resource),
    (r'^api/queue/(?P<name>[^/]+)/', queue_resource),
    (r'^api/queue/', queue_resource),
    (r'^/?$', views.index),
)
