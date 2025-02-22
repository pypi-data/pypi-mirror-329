from dasl_api import api, WorkspaceV1alpha1CreateWorkspaceRequest

from dasl_client.auth.auth import (
    ServiceAccountKeyAuth,
    DatabricksTokenAuth,
    Authorization,
)
from dasl_client.conn.conn import get_base_conn
from dasl_client.core.config import ConfigMixin
from dasl_client.core.datasource import DatasourceMixin
from dasl_client.core.rule import RuleMixin
from dasl_client.core.transform import TransformMixin
from dasl_client.errors.errors import handle_errors


from databricks.sdk.runtime import dbutils


class Client(ConfigMixin, RuleMixin, DatasourceMixin, TransformMixin):
    """
    An Antimatter Security Lakehouse client conn.
    """

    def __init__(self, name: str, email: str, auth: Authorization):
        """
        Initialise a new client.
        """
        self.name = name
        self.email = email
        self.auth = auth

    @staticmethod
    @handle_errors
    def new_client(name: str, email: str) -> "Client":
        """
        Create a new client with the provided name and email and return the associate conn.

        :param self:
        :param name: The proposed name of the client.
        :param email: The email to as the admin contact.
        :return: A client conn.
        :raises:
            ConflictError - If a client with the given name already exists.
            urllib3.exceptions.MaxRetryError - If we failed to establish a connection to the API.
            Exception - Unknown general exception.
        """
        req = WorkspaceV1alpha1CreateWorkspaceRequest(
            admin_user=email, workspace_name=name
        )
        api_client = get_base_conn()
        client = api.WorkspaceV1alpha1Api(api_client=api_client)

        rsp = client.workspace_v1_alpha1_create_workspace(req)
        key = rsp.admin_service_account.apikey
        return Client(name, email, ServiceAccountKeyAuth(name, key))

    @staticmethod
    @handle_errors
    def get_client(name: str, host: str) -> "Client":
        """
        Try build a conn from an existing client, using the databricks
        context token as auth.
        :param name: The name of the client to connect to.
        :param host: An option URL for the DASL server. Will use the default if
                     not supplied.
        :return:
        """
        ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
        api_token = ctx.apiToken().get()
        return Client(name, "", DatabricksTokenAuth(name, api_token, host))
