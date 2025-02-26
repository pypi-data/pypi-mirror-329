"""
Module for Users
https://docs.cloud.f5.com/docs/api/user
"""
from uplink import Consumer, Path, Body, json, get, post, put
from . import helper


@helper.common_decorators
class User(Consumer):
    """Class for Users"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/custom/namespaces/{namespace}/user_roles')
    def list(self, namespace: Path = 'system'):
        """List all Users"""

    @json
    @post('/api/web/custom/namespaces/{namespace}/user_roles')
    def create(self, payload: Body, namespace: Path = 'system'):
        """
        Create a User
        Use create_payload() to build Body
        """

    @json
    @post('/api/web/custom/namespaces/{namespace}/users/cascade_delete')
    def delete(self, payload: Body, namespace: Path = 'system'):
        """
        Delete a User
        use delete_payload() to build Body
        """

    @json
    @put('/api/web/custom/namespaces/{namespace}/users/group_add')
    def group(self, payload: Body, namespace: Path = 'system'):
        """
        Configure Group(s) for a user
        Use group_payload() to build Body
        """

    @json
    @put('/api/web/custom/namespaces/{namespace}/user_roles')
    def update(self, payload: Body, namespace: Path = 'system'):
        """
        Update User Roles
        Use update_payload() to build Body
        """

    @staticmethod
    def create_payload(
            email: str,
            first_name: str,
            last_name: str,
            group_names: list=None,
            namespace_roles: list=None,
            idm_type: str = 'SSO',
            namespace: str = 'system'
        ):
        """Payload for Create"""
        if group_names is None:
            group_names = []
        if namespace_roles is None:
            namespace_roles = []
        return {
            "email": email,
            "first_name": first_name,
            "group_names": group_names,
            "idm_type": idm_type,
            "last_name": last_name,
            "name": email,
            "namespace": namespace,
            "namespace_roles": namespace_roles,
            "type": "USER"
        }

    @staticmethod
    def delete_payload(email: str, namespace: str = 'system'):
        """Payload for delete"""
        return {
            "email": email,
            "namespace": namespace
        }

    @staticmethod
    def group_payload(user: str, group_names: list):
        """
        Payload for group modifications
        *group_names is being replaced
        """
        return {
            "group_names": group_names,
            "username": user
        }
    
    @staticmethod
    def update_payload(email: str, namespace_roles: list, group_names: list, namespace: str = 'system'):
        """
        Payload for user modifications
        *namespace_roles are being replaced
        *group_names are being replaced
        """
        return {
            "email": email,
            "namespace": namespace,
            "namespace_roles": namespace_roles,
            "group_names": group_names
        }
