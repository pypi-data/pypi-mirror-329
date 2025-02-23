#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from msal import ConfidentialClientApplication
from osdu_api.providers.types import BaseCredentials

from osducli.log import get_logger

logger = get_logger(__name__)


class MsalNonInteractiveCredential(BaseCredentials):
    """Get token based client for connecting with OSDU."""

    __access_token = None

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 authority: str,
                 scopes: str,
                 client: ConfidentialClientApplication):
        """Setup the new client

        Args:
            client_id (str): client id for connecting
            authority (str): authority url
            scopes (str): scopes to request
        """
        super().__init__()
        self._msal_confidential_client = client
        self._client_id = client_id
        self._client_secret = client_secret
        self._authority = authority
        self._scopes = scopes

    @property
    def access_token(self) -> str:
        return self.__access_token

    def refresh_token(self) -> str:   # pylint: disable=inconsistent-return-statements
        """
        return access_token.
        """
        token = self._get_token()
        if 'access_token' in token:
            __access_token = token['access_token']
            return __access_token

    def _get_token(self) -> dict:
        """Get token using msal confidential client.

         Returns:
            dict: Dictionary representing the returned token
        """
        result = self._msal_confidential_client.acquire_token_silent([self._scopes], account=None)
        if result:
            return result
        return self._msal_confidential_client.acquire_token_for_client([self._scopes])
