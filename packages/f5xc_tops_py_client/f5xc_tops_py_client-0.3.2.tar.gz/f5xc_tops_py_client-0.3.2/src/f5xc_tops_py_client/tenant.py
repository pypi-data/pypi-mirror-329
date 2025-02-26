"""
Module for Tenant Methods
https://docs.cloud.f5.com/docs/api/tenant
"""
from datetime import datetime
from uplink import Consumer, QueryMap, Path, Body, json, get, post, put, delete # pylint: disable=unused-import
from . import helper

@helper.common_decorators
class Tenant(Consumer):
    """
    Class for Tenant Methods
    """
    def __init__(self, session):
        super().__init__(base_url=session._tenant_url, client=session._session)

    @get('/api/web/namespaces/system/tenant/idm/events/last_login')
    def last_login(self):
        """Lists last login for each user"""

    @get('/api/web/namespaces/system/tenant/idm/events/login')
    def login_events(self, **params: QueryMap):
        """
        Lists login events
        params:
          first: (int) offset
          max: (int) records in response
        """

    @get('api/web/namespaces/system/tenant/idm/users/inactive')
    def list_inactive_users(self):
        """Lists inactive users (90 days without login)"""

    @get('/api/web/namespaces/system/tenant/settings')
    def get_settings(self):
        """Gets tenant settings"""

    @get('/api/web/namespaces/system/tenant/idm/settings')
    def get_idm_settings(self):
        """Gets tenant IDM settings"""

    @json
    @post('/api/web/namespaces/system/tenant/idm/events/login_in_time')
    def login_events_in_tf(self, payload: Body):
        """
        Login events for specified time frame
        Use login_events_in_tf_payload() to build Body
        """

    @staticmethod
    def login_events_in_tf_payload(start: datetime, end: datetime, first: int = 0, maximum: int = 0): # pylint: disable=line-too-long
        """Payload for login_events_in_tf"""
        return {
            "end": helper.xc_format_date(end),
            "first": first,
            "max": maximum,
            "start": helper.xc_format_date(start)
        }
