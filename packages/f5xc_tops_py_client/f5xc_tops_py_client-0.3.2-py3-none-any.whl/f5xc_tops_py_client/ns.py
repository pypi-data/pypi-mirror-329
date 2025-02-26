"""Module for Namespaces"""
from uplink import Consumer, Path, Body, json, get, post # pylint: disable=unused-import
from . import helper


@helper.common_decorators
class NS(Consumer):
    """Class for Namespaces"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/namespaces')
    def list(self):
        """List all Namespaces"""

    @get('/api/web/namespaces/{name}')
    def get(self, name: Path):
        """Get a single Namespace"""

    @json
    @post('/api/web/namespaces')
    def create(self, payload: Body):
        """
        Create a Namespace
        Use create_payload() to build Body
        """

    @json
    @post('/api/web/namespaces/{name}/cascade_delete')
    def delete(self, payload: Body, name: Path):
        """
        Cascade delete a Namespace
        use delete_payload() to build Body
        """

    @staticmethod
    def create_payload(name: str, description: str):
        """Payload for create"""
        return {
            'metadata': {
                'annotations': {},
                'description': description,
                'disable': False,
                'labels': {},
                'name': name,
                'namespace': ''
            },
            'spec': {}
        }

    @staticmethod
    def delete_payload(name: str):
        """Payload for delete"""
        return {
            'name:': name
        }
    