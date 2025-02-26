"""
Module for Load Balancers
https://docs.cloud.f5.com/docs-v2/api/views-http-loadbalancer
https://docs.cloud.f5.com/docs-v2/api/views-tcp-loadbalancer
"""
from uplink import Consumer, Path, Body, get, post, put, delete, json
from . import helper


@helper.common_decorators
class HTTPLoadBalancer(Consumer):
    """
    Class for HTTP Load Balancer API.
    """

    def __init__(self, session):
        """
        Initialize the HTTPLoadBalancer Consumer.
        :param session: Session object with tenant URL and auth.
        """
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/config/namespaces/{namespace}/http_loadbalancers')
    def list(self, namespace: Path):
        """
        List all HTTP Load Balancers in a namespace.
        """

    @get('/api/config/namespaces/{namespace}/http_loadbalancers/{name}')
    def get(self, namespace: Path, name: Path):
        """
        Get details of an HTTP Load Balancer.
        """

    @json
    @post('/api/config/namespaces/{namespace}/http_loadbalancers')
    def create(self, payload: Body, namespace: Path):
        """
        Create an HTTP Load Balancer.
        """

    @json
    @put('/api/config/namespaces/{namespace}/http_loadbalancers/{name}')
    def replace(self, payload: Body, namespace: Path, name: Path):
        """
        Replace an HTTP Load Balancer.
        """

    @delete('/api/config/namespaces/{namespace}/http_loadbalancers/{name}')
    def delete(self, namespace: Path, name: Path):
        """
        Delete an HTTP Load Balancer.
        """

@helper.common_decorators
class TCPLoadBalancer(Consumer):
    """
    Class for TCP Load Balancer API.
    """

    def __init__(self, session):
        """
        Initialize the TCPLoadBalancer Consumer.
        :param session: Session object with tenant URL and auth.
        """
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/config/namespaces/{namespace}/tcp_loadbalancers')
    def list(self, namespace: Path):
        """
        List all TCP Load Balancers in a namespace.
        """

    @get('/api/config/namespaces/{namespace}/tcp_loadbalancers/{name}')
    def get(self, namespace: Path, name: Path):
        """
        Get details of a TCP Load Balancer.
        """

    @json
    @post('/api/config/namespaces/{namespace}/tcp_loadbalancers')
    def create(self, payload: Body, namespace: Path):
        """
        Create a TCP Load Balancer.
        """

    @json
    @put('/api/config/namespaces/{namespace}/tcp_loadbalancers/{name}')
    def replace(self, payload: Body, namespace: Path, name: Path):
        """
        Replace a TCP Load Balancer.
        """

    @delete('/api/config/namespaces/{namespace}/tcp_loadbalancers/{name}')
    def delete(self, namespace: Path, name: Path):
        """
        Delete a TCP Load Balancer.
        """