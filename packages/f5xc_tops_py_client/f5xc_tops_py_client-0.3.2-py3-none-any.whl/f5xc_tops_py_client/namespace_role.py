"""
Module for Namespace Roles
https://docs.cloud.f5.com/docs/api/namespace-role
Need to unwind this class -- not useful
"""
from uplink import Consumer, Path, Body, json, get, post, put # pylint: disable=unused-import
from . import helper


@helper.common_decorators
class NSrole(Consumer):
    """Class for Namespace Roles"""
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/namespaces/{namespace}/namespace_roles')
    def list(self, namespace: Path = 'system'):
        """List all Namespace Roles"""

    @get('/api/web/namespaces/{namespace}/namespace_roles/{name}')
    def get(self, namespace: Path, name: Path,):
        """Get a single Namespace Role"""

    @json
    @post('/api/web/namespaces/{namespace}/namespace_roles')
    def create(self, payload: Body, namespace: Path):
        """
        Create a Namespace Role
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
            namespace: str,
            user: list,
            role: list
        ):
        """Payload for Create"""
        return {
            "metadata": {
                "name": name,
                "namespace": namespace
            },
            "spec": {
                "user": user,
                "role": role
            }
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
