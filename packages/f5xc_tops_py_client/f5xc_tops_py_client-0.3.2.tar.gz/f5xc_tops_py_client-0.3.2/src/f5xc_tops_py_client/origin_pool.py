"""
Module for Origin Pool
https://docs.cloud.f5.com/docs-v2/api/views-origin-pool
"""
from uplink import Consumer, Path, Body, get, post, put, delete, json  # pylint: disable=unused-import
from . import helper


@helper.common_decorators
class OriginPool(Consumer):
    """
    Class for interacting with the Origin Pool API.
    """

    def __init__(self, session):
        """
        Initialize the OriginPool Consumer.
        :param session: Session object with tenant URL and authentication.
        """
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/config/namespaces/{namespace}/origin_pools')
    def list(self, namespace: Path):
        """
        List all Origin Pools in a namespace.
        """

    @get('/api/config/namespaces/{namespace}/origin_pools/{name}')
    def get(self, namespace: Path, name: Path):
        """
        Get details of a specific Origin Pool.
        """

    @json
    @post('/api/config/namespaces/{namespace}/origin_pools')
    def create(self, payload: Body, namespace: Path):
        """
        Create an Origin Pool.
        The payload must be provided by the user.
        """

    @json
    @put('/api/config/namespaces/{namespace}/origin_pools/{name}')
    def replace(self, payload: Body, namespace: Path, name: Path):
        """
        Replace an Origin Pool.
        The payload must be provided by the user.
        """

    @delete('/api/config/namespaces/{namespace}/origin_pools/{name}')
    def delete(self, namespace: Path, name: Path):
        """
        Delete an Origin Pool.
        """