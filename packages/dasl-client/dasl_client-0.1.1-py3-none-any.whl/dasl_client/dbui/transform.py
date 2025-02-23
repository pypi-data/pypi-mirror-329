from dasl_api import (
    DbuiV1TransformRequest,
    DbuiV1TransformRequestInput,
    CoreV1DataSourceAutoloaderSpec,
    DbuiV1TransformRequestTransformsInner,
    DbuiV1TransformResponse,
)

from dasl_client.core.base import BaseMixin
from typing import List, Optional
import dasl_api as openapi_client

from dasl_client.errors.errors import handle_errors
from pydantic import Field


class AdhocTransform(BaseMixin):
    @handle_errors
    def adhoc_transform(
        self,
        warehouse: str,
        preset: str,
        transforms: List[DbuiV1TransformRequestTransformsInner],
        input: Optional[DbuiV1TransformRequestInput] = None,
        autoloader_input: Optional[CoreV1DataSourceAutoloaderSpec] = None,
    ) -> DbuiV1TransformResponse:
        """
        Run a sequence of ADHOC transforms against a SQL warehouse to mimic the operations performed by a datasource.

        :param warehouse: The warehouse ID to run the transforms against.
        :param transforms: The sequence to transforms to run.
        :param input: The source of data to use.
        :param autoloader_input: The autoload specifications.
        :return: a DbuiV1TransformResponse object containing the results after running the transforms.
        :raises: NotFoundError if the rule does not exist
        """
        auth = self.auth.client()
        workspace = self.auth.workspace()
        if autoloader_input is None:
            autoloader_input = Field(default=None, alias="autoloaderInput")
        request = DbuiV1TransformRequest(
            input=input,
            autoloader_input=autoloader_input,
            use_preset=preset,
            transforms=transforms,
        )
        return openapi_client.DbuiV1Api(auth).dbui_v1_transform(
            workspace, warehouse, request
        )
