import abc
from datetime import datetime

from dasl_api import api, WorkspaceV1AuthenticateRequest, ApiClient

from dasl_client.conn.conn import get_base_conn
from dasl_client.errors.errors import handle_errors

from typing import Optional

# The minimum age of a conn that we allow. Generally, clients are issued for
# a small batch of operations (one or two requests), not long-running
# operations. This threshold should be tuned to the longest expected operation
# using a single conn.
EXPIRY_OVERLAP_SECONDS = 600


class Authorization(abc.ABC):
    """
    A common interface for Authentication
    """

    @abc.abstractmethod
    def client(self) -> ApiClient:
        raise NotImplementedError("conn method must be implemented")

    def workspace(self) -> str:
        raise NotImplementedError("client method must be implemented")


class ServiceAccountKeyAuth(Authorization):
    """
    Authorisation implementation for Service Account Keys
    """

    def __init__(
        self, workspace: str, service_account_key: str, host: Optional[str] = None
    ):
        self._workspace = workspace
        self._service_account_key = service_account_key
        self._client = get_base_conn(host=host)
        self.expiry: int = int(datetime.now().timestamp())

    def client(self) -> ApiClient:
        """
        Return an API conn that can be used to issue an API request to the
        configured host. The associated bearer token is valid for at least
        EXPIRY_OVERLAP_SECONDS.
        :return: An API conn with valid auth
        """
        if int(datetime.now().timestamp()) > self.expiry - EXPIRY_OVERLAP_SECONDS:
            self.refresh()
        return self._client

    def workspace(self) -> str:
        """
        Return the client associated with this Service Account Key
        :return: The client name.
        """
        return self._workspace

    @handle_errors
    def refresh(self):
        """
        A helper function to refresh the bearer token used for authentication.
        :return:
        """
        req = WorkspaceV1AuthenticateRequest(
            service_account_key=self._service_account_key
        )
        handler = api.WorkspaceV1Api(api_client=self._client)

        resp = handler.workspace_v1_authenticate(
            workspace=self._workspace, workspace_v1_authenticate_request=req
        )
        self._client.set_default_header("Authorization", f"Bearer {resp.token}")
        verification = api.DbuiV1Api(self._client).dbui_v1_verify_auth()
        self.expiry = verification.expiry


class DatabricksTokenAuth(Authorization):
    """
    Authorisation implementation fo using Databricks Tokens
    """

    def __init__(self, workspace: str, token: str, host: Optional[str] = None):
        self._workspace = workspace
        self._databricks_token = token
        self._client = get_base_conn(host=host)
        self.expiry: int = int(datetime.now().timestamp())

    def client(self) -> ApiClient:
        """
        Return an API conn that can be used to issue an API request to the
        configured host. The associated bearer token is valid for at least
        EXPIRY_OVERLAP_SECONDS.
        :return: An API conn with valid auth
        """
        if int(datetime.now().timestamp()) > self.expiry - EXPIRY_OVERLAP_SECONDS:
            self.refresh()
        return self._client

    def workspace(self) -> str:
        """
        Return the client associated with this Databricks Token
        :return: The client name.
        """
        return self._workspace

    @handle_errors
    def refresh(self):
        """
        A helper function to refresh the bearer token used for authentication.
        :return:
        """
        req = WorkspaceV1AuthenticateRequest(
            databricks_api_token=self._databricks_token
        )
        handler = api.WorkspaceV1Api(api_client=self._client)

        resp = handler.workspace_v1_authenticate(
            workspace=self._workspace, workspace_v1_authenticate_request=req
        )
        self._client.set_default_header("Authorization", f"Bearer {resp.token}")
        verification = api.DbuiV1Api(self._client).dbui_v1_verify_auth()
        self.expiry = verification.expiry
