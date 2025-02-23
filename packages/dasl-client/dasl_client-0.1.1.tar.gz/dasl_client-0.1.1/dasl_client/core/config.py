from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel

import dasl_api as openapi_client
from dasl_api import (
    WorkspaceV1WorkspaceConfig,
    WorkspaceV1WorkspaceConfigSpec,
    WorkspaceV1WorkspaceConfigSpecSystemTablesConfig,
    WorkspaceV1ExportConfig,
    WorkspaceV1WorkspaceConfigSpecObservables,
    WorkspaceV1WorkspaceConfigSpecComputeGroupLimitsInner,
    WorkspaceV1WorkspaceConfigSpecDefaultConfig,
    WorkspaceV1WorkspaceConfigSpecManagedRetentionInner,
    WorkspaceV1WorkspaceConfigSpecDetectionRuleMetadata,
    CommonV1ObjectMeta,
    WorkspaceV1AdminConfig,
    WorkspaceV1AdminConfigSpec,
    WorkspaceV1AdminConfigSpecAuth,
    WorkspaceV1AdminConfigSpecAuthServicePrincipal,
    WorkspaceV1AdminConfigSpecAuthAppClientId,
)

from dasl_client.core.base import BaseMixin
from dasl_client.errors.errors import handle_errors


class AdminConfig(BaseModel):
    host: str
    client_id: str
    service_principal_id: str
    service_principal_secret: str


class ConfigMixin(BaseMixin):
    """
    Client mixin for CRUD operations on config
    """

    @handle_errors
    def get_config(self) -> WorkspaceV1WorkspaceConfig:
        """
        Get the current configuration for the client.

        :return: WorkspaceV1WorkspaceConfig object
        :exception: NotFoundError if the client does not have a configuration.
        """
        auth = self.auth.client()
        workspace = self.auth.workspace()
        client = openapi_client.WorkspaceV1Api(auth)
        return client.workspace_v1_get_config(workspace)

    @handle_errors
    def put_admin_config(self, config: AdminConfig) -> WorkspaceV1AdminConfig:
        """
        Update the admin configuration for the client.

        :param host: The url of the databricks client instance.
        :param service_principal_id: The ID of the databricks service principal.
        :param service_principal_secret: The  databricks service principal secret.
        :param client_id: The databricks conn ID.
        :return: The WorkspaceV1AdminConfig after applying the configuration
        """
        api_auth = self.auth.client()
        workspace = self.auth.workspace()
        client = openapi_client.WorkspaceV1Api(api_auth)

        auth = WorkspaceV1AdminConfigSpecAuth(
            host=config.host,
            service_principal=WorkspaceV1AdminConfigSpecAuthServicePrincipal(
                client_id=config.service_principal_id,
                secret=config.service_principal_secret,
            ),
            app_client_id=WorkspaceV1AdminConfigSpecAuthAppClientId(
                client_id=config.client_id
            ),
        )

        req = WorkspaceV1AdminConfig(
            api_version="v1",
            kind="WorkspaceConfig",
            spec=WorkspaceV1AdminConfigSpec(auth=auth),
        )

        return client.workspace_v1_put_admin_config(workspace, req)

    @handle_errors
    def put_config(
        self,
        system_tables_catalog_name: str = "",
        system_tables_schema: str = "",
        default_sql_warehouse: Optional[str] = None,
        detection_categories: Optional[List[str]] = None,
        notable_export: Optional[WorkspaceV1ExportConfig] = None,
        operational_alert_export: Optional[WorkspaceV1ExportConfig] = None,
        observables: Optional[WorkspaceV1WorkspaceConfigSpecObservables] = None,
        compute_group_limits: Optional[
            List[WorkspaceV1WorkspaceConfigSpecComputeGroupLimitsInner]
        ] = None,
        dasl_storage_path: Optional[str] = None,
        default_config: Optional[
            WorkspaceV1WorkspaceConfigSpecDefaultConfig
        ] = None,
        managed_retention: Optional[
            List[WorkspaceV1WorkspaceConfigSpecManagedRetentionInner]
        ] = None,
    ) -> None:
        """
        Update the configuration for the client.

        :param system_tables_catalog_name: The catalog in Databricks under which system tables should be stored.
        :param system_tables_schema: The catalog schema in Databricks under which system tables should be stored.
        :param default_sql_warehouse: The default SQL warehouse for DASL to use.
        :param detection_categories:
        :param notable_export: Optional parameters to enable exporting of notables.
        :param operational_alert_export: Optional parameters to enable exporting of operations alerts.
        :param observables: Observables that can be collected when generating rules.
        :param compute_group_limits: Limit to apply to compute groups.
        :param dasl_storage_path: The root path under which DASL resources will be stored.
        :param default_config: the default configuration for DASL resources.
        :param managed_retention: Retention characteristics to apply to generated data.
        :return: The config object as recorded by the server.
        """
        spec = WorkspaceV1WorkspaceConfigSpec(
            system_tables_config=WorkspaceV1WorkspaceConfigSpecSystemTablesConfig(
                catalog_name=system_tables_catalog_name,
                var_schema=system_tables_schema,
            ),
            default_sql_warehouse=default_sql_warehouse,
            notable_export=notable_export,
            operational_alert_export=operational_alert_export,
            observables=observables,
            compute_group_limits=compute_group_limits,
            dasl_storage_path=dasl_storage_path,
            default_config=default_config,
            managed_retention=managed_retention,
        )

        if detection_categories is not None:
            spec.detection_rule_metadata = (
                WorkspaceV1WorkspaceConfigSpecDetectionRuleMetadata(
                    detection_categories=detection_categories
                )
            )

        auth = self.auth.client()
        workspace = self.auth.workspace()

        metadata = CommonV1ObjectMeta(workspace=workspace, name="config")
        request = WorkspaceV1WorkspaceConfig(
            api_version="v1", kind="WorkspaceConfig", metadata=metadata, spec=spec
        )
        client = openapi_client.WorkspaceV1Api(auth)
        client.workspace_v1_put_config(workspace, request)
