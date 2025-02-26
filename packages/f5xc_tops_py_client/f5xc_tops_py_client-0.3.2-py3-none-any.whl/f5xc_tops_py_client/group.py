"""Module for Groups"""
from uplink import Consumer, Path, Body, json, get, post, put # pylint: disable=unused-import
from . import helper


@helper.common_decorators
class Group(Consumer):
    """Class for Groups"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/custom/namespaces/{namespace}/user_groups')
    def list(self, namespace: Path = 'system'):
        """List all Groups"""

    @get('/api/web/namespaces/{namespace}/user_groups/{name}')
    def get(self, name: Path, namespace: Path = 'system'):
        """Get a single Group"""

    @json
    @post('/api/web/custom/namespaces/{namespace}/user_groups')
    def create(self, payload: Body, namespace: Path = 'system'):
        """
        Create a Group
        Use create_payload() to build Body
        """

    @json
    @post('/api/web/custom/namespaces/{namespace}/user_groups/{name}')
    def delete(self, name: Path, namespace: Path = 'system'):
        """Delete a group"""

    @json
    @put('/api/web/custom/namespaces/{namespace}/user_groups/{name}/assign_namespace_roles')
    def role_assign(self, payload: Body, name: Path, namespace: Path = 'system'):
        """
        Assign roles for a group
        Use role_payload() to build Body
        """

    @json
    @put('/api/web/custom/namespaces/{namespace}/user_groups/{name}/remove_namespace_roles')
    def role_remove(self, payload: Body, name: Path, namespace: Path = 'system'):
        """
        Remove roles for a group
        Use role_payload() to build Body
        """

    @staticmethod
    def create_payload(
            name: str,
            description: str,
            display_name: str,
            namespace_roles: list,
            usernames: list,
        ):
        """Payload for Create"""
        return {
            "description": description,
            "display_name": display_name,
            "name": name,
            "namespace_roles": namespace_roles,
            "sync_id": "string",
            "usernames": usernames
        }

    @staticmethod
    def role_payload(
            name: str,
            namespace_roles: list
        ):
        """
        Payload for role modifications
        *namespace_roles are added/deleted based on method
        """
        return {
            "name": name,
            "namespace_roles": namespace_roles
        }
