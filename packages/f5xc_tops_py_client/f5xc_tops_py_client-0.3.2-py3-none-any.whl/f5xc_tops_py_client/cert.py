"""Module for Certificate"""
from uplink import Consumer, Path, Body, json, get, post, put, delete #pylint: disable=unused-import
from . import helper


@helper.common_decorators
class Cert(Consumer):
    """Class for Certificates"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/config/namespaces/{namespace}/certificates')
    def list(self, namespace: Path):
        """List all Certificates in an NS"""

    @get('/api/config/namespaces/{namespace}/certificates/{name}')
    def get(self, name: Path, namespace: Path):
        """Get a Certificate"""

    @json
    @post('/api/config/namespaces/{namespace}/certificates')
    def create(self, payload: Body, namespace: Path):
        """Create a Certificate"""

    @json
    @put('/api/config/namespaces/{namespace}/certificates/{name}')
    def replace(self, payload: Body, name: Path, namespace: Path):
        """Replace a Certificate"""

    @json
    @delete('/api/config/namespaces/{namespace}/certificates/{name}')
    def delete(self, payload: Body, name: Path, namespace: Path):
        """Delete a Certificate"""

    @staticmethod
    def create_payload(name: str, namespace: str, cert: str, key: str):
        """
        Payload for create or replace cert
        {cert} and {key} must be b64 encoded
        """
        return {
            'metadata': {
                'name': name,
                'namespace': namespace,
                'disable': False
            },
            'spec': {
                'certificate_url': f'string:///{cert}',
                'private_key': {
                    'clear_secret_info': {
                        'url': f'string:///{key}'
                    }
                }
            }
        }

    @staticmethod
    def delete_payload(name: str, namespace: str, fail_if_referred: bool = True):
        """Payload for delete"""
        return {
            "fail_if_referred": fail_if_referred,
            "name": name,
            "namespace": namespace
        }
