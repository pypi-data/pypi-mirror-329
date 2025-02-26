"""
Module for Roles
https://docs.cloud.f5.com/docs/api/role
"""
from uplink import Consumer, Path, Body, json, get, post, put, delete # pylint: disable=unused-import
from . import helper


@helper.common_decorators
class Role(Consumer):
    """
    Class for Roles
    "custom" endpoints in use for list(), get(), create()
    """
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/custom/namespaces/{namespace}/roles')
    def list(self, namespace: Path ='system'):
        """List all Roles"""

    @get('/api/web/namespaces/{namespace}/roles')
    def listv1(self, namespace: Path = 'system'):
        """List all Roles"""

    @json
    @post('/api/web/custom/namespaces/{namespace}/roles')
    def create(self, payload: Body, namespace: Path = 'system'):
        """
        Create a Role
        Use create_payload() to build Body
        """

    @json
    @put('/api/web/custom/namespaces/{namespace}/roles/{name}')
    def replace(self, payload: Body, name: Path, namespace: Path = 'system'):
        """
        Replace Role
        Use replace_payload to build Body
        """

    @json
    @delete('/api/web/namespaces/{namespace}/roles/{name}')
    def delete(self, payload: Body, name: Path, namespace: Path = 'system'):
        """
        Delete a Role
        use delete_payload() to build Body
        ISSUE: Console shows no payload here
        """

    @staticmethod
    def create_payload(
            name: str,
            description: str,
            api_groups: list,
            labels = None
        ):
        """Payload for Create"""
        if labels is None:
            labels = {}
        return {
            "api_groups": api_groups,
            "metadata": {
                "annotations": {},
                "description": description,
                "disable": False,
                "labels": labels,
                "name": name,
                "namespace": "system"
            },
            "namespace": "system",
            "spec": {}
        }

    @staticmethod
    def replace_payload(name: str, api_groups: list):
        """
        Payload for Role modifications
        *api_groups is being replaced
        """
        return {
            "api_groups": api_groups,
            "name": name,
            "namespace": "system",
            "spec": {}
        }

    @staticmethod
    def delete_payload(name: str):
        """Payload for delete"""
        return {
            "fail_if_referred": True,
            "name": name,
            "namespace": "system"
        }
