"""
Module for Registration Methods
https://docs.cloud.f5.com/docs/api/registration
"""
from uplink import Consumer, Path, Body, json, get, post #pylint: disable=unused-import
from . import helper

@helper.common_decorators
class Registration(Consumer):
    """
    Class for Tenant Methods
    """
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/register/namespaces/{namespace}/registrations')
    def list(self, namespace: Path ='system'):
        """List Registrations"""

    @json
    @post('/api/register/namespaces/{namespace}/listregistrationsbystate')
    def list_by_state(self, payload: Body, namespace: Path ='system'):
        """
        List Registrations by state
        Use list_by_state_payload() to build Body
        """

    @get('/api/register/namespaces/{namespace}/registrations/{name}')
    def get(self, name: Path, namespace: Path ='system'):
        """Get a single Registration"""

    @json
    @post('/api/register/namespaces/{namespace}/registration/{name}/approve')
    def approve(self, payload: Body, name: Path, namespace: Path ='system'):
        """
        Approve a pending registration
        Use approve_payload() to build Body
        """

    @staticmethod
    def list_by_state_payload(state: str = 'NEW', namespace: str = 'system') -> dict:
        """
        Payload for list_by_state
        """
        return {
            "namespace": namespace,
            "state": state
        }

    @staticmethod
    def approve_payload(name: str, passport: dict, state: str = 'APPROVED', namespace: str = 'system') -> dict: # pylint: disable=line-too-long
        """
        Payload for approve
        pass 'passport' dict from get()
        """
        return {
            "namespace": namespace,
            "name": name,
            "state": state,
            "passport" : passport
    }

    @staticmethod
    def _get_reg_name(obj: dict) -> str:
        """
        Takes a registration object, returns the name
        """
        return obj['name']

    @staticmethod
    def _get_reg_token(obj: dict) -> str:
        """
        Takes a registration object, returns the name
        """
        return obj['get_spec']['token']

    @staticmethod
    def _get_passport(obj: dict) -> dict:
        """
        Takes a registration object, returns the passport
        """
        return obj['get_spec']['passport']

    @staticmethod
    def _get_cluster_name(obj: dict) -> str:
        """
        Takes a registration object, returns the passport
        """
        return obj['get_spec']['passport']['cluster_name']
