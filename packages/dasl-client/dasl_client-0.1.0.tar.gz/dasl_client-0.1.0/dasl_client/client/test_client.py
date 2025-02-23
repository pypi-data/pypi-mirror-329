import random
import string
import time
import unittest

from dasl_api import (
    WorkspaceV1WorkspaceConfigSpecObservables,
    WorkspaceV1WorkspaceConfigSpecObservablesKindsInner,
    WorkspaceV1WorkspaceConfigSpecDefaultConfig,
    WorkspaceV1DefaultConfig,
    CoreV1Schedule,
    CoreV1RuleSpecInput,
    CoreV1RuleSpecOutput,
    CoreV1RuleSpecInputStream,
    CoreV1RuleSpecInputStreamTablesInner,
    CoreV1RuleObservable,
    CoreV1RuleObservableRisk,
    CoreV1DataSourceSpecSilver,
    CoreV1DataSourceSpecGold,
    CoreV1DataSourceSpecSilverPreTransform,
    CoreV1DataSourceSpecBronze,
)

from dasl_client.client.client import Client


class MyTestCase(unittest.TestCase):
    @staticmethod
    def create_workspace(self, email) -> Client:
        workspace_name = "".join(random.choices(string.ascii_lowercase, k=16))
        workspace = Client.new_client(workspace_name, email)

        workspace.put_admin_config(
            host="https://dbc-958e1220-59fc.cloud.databricks.com",
            client_id="22853b93-68ba-4ae2-8e41-976417f501dd",
            service_principal_id="",
            service_principal_secret="",
        )

        workspace.put_config(
            system_tables_catalog_name="databricks_dev",
            system_tables_schema="asl_system_tables",
            detection_categories=["example"],
            observables=WorkspaceV1WorkspaceConfigSpecObservables(
                kinds=[
                    WorkspaceV1WorkspaceConfigSpecObservablesKindsInner(
                        name="ip_source",
                        sql_type="string",
                    ),
                    WorkspaceV1WorkspaceConfigSpecObservablesKindsInner(
                        name="ip_destination",
                        sql_type="string",
                    ),
                ],
                relationships=["tenant", "tenant"],
            ),
            dasl_storage_path="/Volumes/databricks_dev/default/test-itg",
            default_config=WorkspaceV1WorkspaceConfigSpecDefaultConfig(
                datasources=WorkspaceV1DefaultConfig(
                    notebook_location="/Workspace/Shared/datasources/notebooks",
                    bronze_schema="bronze",
                    silver_schema="silver",
                    gold_schema="gold",
                    catalog_name="default",
                ),
                transforms=WorkspaceV1DefaultConfig(
                    notebook_location="/Workspace/Shared/transforms/notebooks",
                    bronze_schema="bronze",
                    silver_schema="silver",
                    gold_schema="gold",
                    catalog_name="default",
                ),
                rules=WorkspaceV1DefaultConfig(
                    notebook_location="/Workspace/Shared/rules/notebooks",
                    bronze_schema="bronze",
                    silver_schema="silver",
                    gold_schema="gold",
                    catalog_name="default",
                ),
                var_global=WorkspaceV1DefaultConfig(
                    bronze_schema="bronze",
                    silver_schema="silver",
                    gold_schema="gold",
                    catalog_name="default",
                ),
            ),
        )
        return workspace

    def test_create_rule(self):
        workspace = self.create_workspace(self, "sean@antimatter.io")
        rule_name_1 = f"{workspace.name}-rule-1"

        workspace.create_rule(
            name=rule_name_1,
            schedule=CoreV1Schedule(at_least_every="2h"),
            input=CoreV1RuleSpecInput(
                stream=CoreV1RuleSpecInputStream(
                    filter="ip_count > 999",
                    tables=[
                        CoreV1RuleSpecInputStreamTablesInner(
                            name="databricks_dev.antimatter_meta.test_ip_summaries",
                            alias="ip",
                        ),
                        CoreV1RuleSpecInputStreamTablesInner(
                            name="databricks_dev.antimatter_meta.server_load",
                            join_expr="ip.region_id = server.region_id",
                            join_type="inner",
                            alias="server",
                        ),
                    ],
                )
            ),
            output=CoreV1RuleSpecOutput(
                summary="rule 1: we found {ip_count} unique IPs",
                context={
                    "IP count": "{ip_count}",
                    "Comment is:": "context: user, comment: {comment}",
                },
            ),
            observables=[
                CoreV1RuleObservable(
                    kind="ip_source",
                    value="ip_count",
                    relationship="tenant",
                    risk=CoreV1RuleObservableRisk(
                        impact="ip_count/1000", confidence="80"
                    ),
                ),
                CoreV1RuleObservable(
                    kind="ip_destination",
                    value="ip_count",
                    relationship="tenant",
                    risk=CoreV1RuleObservableRisk(
                        impact="ip_count/1000", confidence="80"
                    ),
                ),
            ],
        )

        while workspace.get_rule(rule_name_1).status is None:
            time.sleep(2)
        self.assertEqual(workspace.get_rule(rule_name_1).status.job_status, "scheduled")
        time.sleep(5)
        workspace.delete_rule(rule_name_1)

    def test_create_datasource(self):
        workspace = self.create_workspace(self, "sean@antimatter.io")
        datasource_name = f"{workspace.name}-datasource"

        s = CoreV1DataSourceSpecSilver(
            pre_transform=CoreV1DataSourceSpecSilverPreTransform(
                use_preset="aws_sec_lake_route53",
            )
        )

        workspace.create_datasource(
            name=datasource_name,
            schedule=CoreV1Schedule(at_least_every="2h"),
            source="aws",
            source_type="route53",
            use_preset="aws",
            bronze=CoreV1DataSourceSpecBronze(bronze_table="aws_route53_data"),
            silver=CoreV1DataSourceSpecSilver(
                pre_transform=CoreV1DataSourceSpecSilverPreTransform(
                    use_preset="aws_sec_lake_route53",
                )
            ),
            gold=CoreV1DataSourceSpecGold(),
        )

        while workspace.get_datasource(datasource_name).status is None:
            time.sleep(2)
        self.assertEqual(
            workspace.get_datasource(datasource_name).status.job_status, "scheduled"
        )
        time.sleep(5)
        workspace.delete_datasource(datasource_name)


if __name__ == "__main__":
    unittest.main()
