"""Module for API Credentials"""
from uplink import Consumer, Path, Body, json, get, post
from . import helper


@helper.common_decorators
class APIcred(Consumer):
    """Class for API Credentials"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/namespaces/{namespace}/api_credentials')
    def list(self, namespace: Path = 'system'):
        """List all API Credentials"""

    @get('/api/web/namespaces/{namespace}/api_credentials/{name}')
    def get(self, name: Path, namespace: Path = 'system'):
        """Get a single API Credential"""

    @json
    @post('/api/web/namespaces/{namespace}/api_credentials')
    def create(self, payload: Body, namespace: Path = 'system'):
        """
        Create an API Credential
        Use create_payload() to build Body
        """

    @json
    @post('api/web/namespaces/{namespace}/renew/api_credentials')
    def renew(self, payload: Body, namespace: Path = 'system'):
        """
        Renew an API Credential
        Use renew_payload() to build Body
        """

    @json
    @post('/api/web/namespaces/{namespace}/revoke/api_credentials')
    def revoke(self, payload: Body, namespace: Path = 'system'):
        """
        Revoke an API Credential
        Use revoke_payload() to build Body
        """

    @staticmethod
    def create_payload(name: str, expiration_days: int, namespace: str = 'system'):
        """Payload for create"""
        return {
            'spec': {
                'type': 'API_TOKEN'
            },
            'namespace': namespace,
            'name': name,
            'expiration_days': expiration_days
        }

    @staticmethod
    def renew_payload(name: str, expiration_days: int, namespace: str = 'system'):
        """Payload for renew"""
        return {
            'expiration_days': expiration_days,
            'name': name,
            'namespace': namespace
        }

    @staticmethod
    def revoke_payload(name: str, namespace: str = 'system'):
        """Payload for revoke """
        return {
            'name': name,
            'namespace': namespace
        }


@helper.common_decorators
class SVCcred(Consumer):
    """Class for Service Credentials"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/namespaces/{namespace}/service_credentials')
    def list(self, namespace: Path = 'system'):
        """List all Service Credentials"""

    @json
    @post('/api/web/namespaces/{namespace}/service_credentials')
    def create(self, payload: Body, namespace: Path = 'system'):
        """
        Create an Service Credential
        Use create_payload() to build Body
        """

    @json
    @post('api/web/namespaces/{namespace}/renew/service_credentials')
    def renew(self, payload: Body, namespace: Path = 'system'):
        """
        Renew a Service Credential
        Use renew_payload() to build Body
        """

    @json
    @post('/api/web/namespaces/{namespace}/revoke/service_credentials')
    def revoke(self, payload: Body, namespace: Path = 'system'):
        """
        Revoke a Service Credential
        Use revoke_payload() to build Body
        """

    @staticmethod
    def create_payload(
        name: str,
        namespace_roles: list,
        expiration_days: int,
        namespace: str = 'system'
        ):
        """Payload for create"""
        return {
            'type':'SERVICE_API_TOKEN',
            'namespace': namespace,
            'name': name,
            'namespace_roles': namespace_roles,
            'expiration_days': expiration_days
        }

    @staticmethod
    def renew_payload(name: str, expiration_days: int, namespace: str = 'system'):
        """payload for renew"""
        return {
            'expiration_days': expiration_days,
            'name': name,
            'namespace': namespace
        }

    @staticmethod
    def revoke_payload(name: str, namespace: str = 'system'):
        """Payload for revoke"""
        return {
            'name': name,
            'namespace': namespace
        }
    