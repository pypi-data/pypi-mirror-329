"""Module providing XC session"""
from urllib.parse import urlparse
import requests
from . import helper

class Session:
    """Class providing request session with auth"""
    def __init__(self, tenant_url=None, api_token=None, validate=True):
        self._tenant_url = self.validate_url(tenant_url)
        self._api_token = api_token
        self._session = requests.Session()
        self._session.headers.update({'Authorization': f'APIToken {self._api_token}'})
        if validate:
            self.whoami()

    def whoami(self) -> None:
        """Method to check if we have a valid session"""
        try:
            r = self._session.get(self._tenant_url + '/api/web/custom/namespaces/system/whoami')
            r.raise_for_status()
        except Exception as e:
            raise helper.TopsXCException("Invalid Token") from e

    @staticmethod
    def validate_url(url) -> str:
        """Method to validate the tenant URL."""
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            stripped_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rstrip('/')}"
        else:
            raise helper.TopsXCException("Invalid Tenant URL")
        return stripped_url
        