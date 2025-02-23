from typing import Optional

from dasl_api import (
    api,
    WorkspaceV1AdminConfigSpec,
    WorkspaceV1CreateWorkspaceRequest,
    WorkspaceV1AdminConfigSpecAuth,
    WorkspaceV1AdminConfigSpecAuthAppClientId,
    WorkspaceV1AdminConfigSpecAuthServicePrincipal,
)

from dasl_client.auth.auth import (
    ServiceAccountKeyAuth,
    DatabricksTokenAuth,
    Authorization,
)
from dasl_client.conn.conn import get_base_conn
from dasl_client.core.config import AdminConfig, ConfigMixin
from dasl_client.core.datasource import DatasourceMixin
from dasl_client.dbui.transform import AdhocTransform
from dasl_client.core.rule import RuleMixin
from dasl_client.core.transform import TransformMixin
from dasl_client.errors.errors import ConflictError, handle_errors

from databricks.sdk.runtime import dbutils


class Client(ConfigMixin, RuleMixin, DatasourceMixin, TransformMixin, AdhocTransform):
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
    def new_client(
        name: str,
        email: str,
        config: AdminConfig,
    ) -> "Client":
        """
        Create a new client with the provided name and email and return the associate conn.

        :param self:
        :param name: The proposed name of the client.
        :param email: The email to as the admin contact.
         :param config: admin config settings for access to Databricks.
        :return: A client conn.
        :raises:
            ConflictError - If a client with the given name already exists.
            urllib3.exceptions.MaxRetryError - If we failed to establish a connection to the API.
            Exception - Unknown general exception.
        """
        req = WorkspaceV1CreateWorkspaceRequest(
            admin_user=email,
            workspace_name=name,
            admin_config=WorkspaceV1AdminConfigSpec(
                auth=WorkspaceV1AdminConfigSpecAuth(
                    host=config.host,
                    app_client_id=WorkspaceV1AdminConfigSpecAuthAppClientId(
                        client_id=config.client_id,
                    ),
                    service_principal=WorkspaceV1AdminConfigSpecAuthServicePrincipal(
                        client_id=config.service_principal_id,
                        secret=config.service_principal_secret,
                    ),
                ),
            ),
        )
        api_client = get_base_conn()
        client = api.WorkspaceV1Api(api_client=api_client)

        rsp = client.workspace_v1_create_workspace(req)
        key = rsp.admin_service_account.apikey
        return Client(name, email, ServiceAccountKeyAuth(name, key))

    @staticmethod
    @handle_errors
    def get_client(name: str, host: str, service_account_token: Optional[str] = None) -> "Client":
        """
        Try build a conn from an existing client, using the databricks
        context token as auth.
        :param name: The name of the client to connect to.
        :param host: An option URL for the DASL server. Will use the default if
                     not supplied.
        :param service_account_token: Optional service account token. if
               provided we will attempt to make a client form this.
        :return:
        """
        if service_account_token is not None:
            return Client(name, "", ServiceAccountKeyAuth(name, service_account_token))
        ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
        api_token = ctx.apiToken().get()
        return Client(name, "", DatabricksTokenAuth(name, api_token, host))

    @staticmethod
    @handle_errors
    def new_or_existing_client(
        name: str,
        email: str,
        host: str,
        config: AdminConfig,
    ) -> "Client":
        """
        Create a new client with the provided name and email and return
        the associate conn, or if the workspace already exists, connect
        to it using the provided name and host.

        :param self:
        :param name: The proposed name of the client.
        :param email: The email to as the admin contact.
        :param host: An option URL for the DASL server. Will use the default if
                     not supplied.
        :param config: admin config settings. If creating a new workspace,
            these will be sent with the request. If the workspace already
            exists, the workspace admin config will be updated.
        :return: A client conn.
        :raises:
            urllib3.exceptions.MaxRetryError - If we failed to establish a connection to the API.
            Exception - Unknown general exception.
        """
        try:
            return Client.new_client(name, email, config)
        except ConflictError:
            result = Client.get_client(name, host)
            result.put_admin_config(config)
            return result
