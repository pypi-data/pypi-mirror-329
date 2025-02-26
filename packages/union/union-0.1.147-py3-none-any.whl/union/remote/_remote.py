import datetime
import logging
import os
import typing
from typing import Optional, Union

from flyteidl.core import artifact_id_pb2 as art_id
from flyteidl.service.identity_pb2 import UserInfoRequest, UserInfoResponse
from flyteidl.service.identity_pb2_grpc import IdentityServiceStub
from flytekit import BlobType
from flytekit.clients.friendly import SynchronousFlyteClient
from flytekit.configuration import Config
from flytekit.core.artifact import ArtifactQuery, Partitions, TimePartition
from flytekit.core.type_engine import LiteralsResolver, TypeEngine
from flytekit.exceptions import user as user_exceptions
from flytekit.exceptions.user import FlyteEntityNotExistException
from flytekit.models.literals import Blob, BlobMetadata, Literal, Scalar
from flytekit.remote import FlyteRemote
from flytekit.remote.entities import FlyteLaunchPlan, FlyteTask, FlyteWorkflow
from flytekit.remote.executions import FlyteNodeExecution, FlyteTaskExecution, FlyteWorkflowExecution
from flytekit.tools.translator import Options

from union._config import (
    _DEFAULT_DOMAIN,
    _DEFAULT_PROJECT_BYOC,
    ConfigSource,
    ConfigWithSource,
    _config_from_api_key,
    _get_config_obj,
    _get_default_project,
    _get_organization,
)
from union._interceptor import update_client_with_interceptor
from union.app._models import App
from union.artifacts import Artifact
from union.artifacts._utils import construct_search_artifact_request
from union.internal.app.app_definition_pb2 import App as AppIDL
from union.internal.artifacts import artifacts_pb2, artifacts_pb2_grpc
from union.internal.imagebuilder import definition_pb2 as image_definition__pb2
from union.internal.imagebuilder import payload_pb2 as image_payload__pb2
from union.internal.imagebuilder import service_pb2_grpc as image_service_pb2_grpc

SERVERLESS_VANITY_URLS = {
    "https://serverless-1.us-east-2.s.union.ai": "https://serverless.union.ai",
    "https://serverless-preview.canary.unionai.cloud": "https://serverless.canary.union.ai",
    "https://serverless-gcp.cloud-staging.union.ai": "https://serverless.staging.union.ai",
}


class UnionRemote(FlyteRemote):
    def __init__(
        self,
        config: typing.Optional[Union[Config, str]] = None,
        default_project: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = _DEFAULT_DOMAIN,
        data_upload_location: str = "flyte://my-s3-bucket/",
        **kwargs,
    ):
        from union._config import _get_image_builder_priority
        from union.ucimage._image_builder import _register_union_image_builder

        if config is None:
            config = _get_config_obj(config, default_to_union_semantics=True)
        else:
            config_with_source = ConfigWithSource(config=config, source=ConfigSource.REMOTE)
            config = _get_config_obj(config_with_source, default_to_union_semantics=True)

        if default_project is None:
            default_project = _get_default_project(_DEFAULT_PROJECT_BYOC, cfg_obj=config)

        # register Union image builder when getting remote so it's available for
        # jupyter notebook task and workflow execution.
        _register_union_image_builder(_get_image_builder_priority(config.platform.endpoint))

        super().__init__(config, default_project, default_domain, data_upload_location, **kwargs)
        self._artifacts_client = None
        self._images_client = None

        from union.remote._app_remote import AppRemote

        self._app_remote = AppRemote(union_remote=self, default_project=default_project, default_domain=default_domain)

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        default_project: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = _DEFAULT_DOMAIN,
        data_upload_location: str = "flyte://my-s3-bucket/",
        **kwargs,
    ) -> "UnionRemote":
        """Call this if you want to directly instantiate a UnionRemote from an API key"""
        return cls(
            config=_config_from_api_key(api_key),
            default_project=default_project,
            default_domain=default_domain,
            data_upload_location=data_upload_location,
            **kwargs,
        )

    @property
    def client(self) -> SynchronousFlyteClient:
        """Return a SynchronousFlyteClient for additional operations."""
        if not self._client_initialized:
            client = SynchronousFlyteClient(self.config.platform, **self._kwargs)
            org = _get_organization(self.config.platform, channel=client._channel)
            self._client = update_client_with_interceptor(client, org)
            self._client_initialized = True

        return self._client

    def generate_console_http_domain(self) -> str:
        default_console_http_domain = super().generate_console_http_domain()
        return SERVERLESS_VANITY_URLS.get(default_console_http_domain, default_console_http_domain)

    def generate_console_url(
        self,
        entity: typing.Union[
            FlyteWorkflowExecution,
            FlyteNodeExecution,
            FlyteTaskExecution,
            FlyteWorkflow,
            FlyteTask,
            FlyteLaunchPlan,
            Artifact,
        ],
    ):
        """
        Generate a UnionAI console URL for the given Flyte remote endpoint.
        It will also handle Union AI specific entities like Artifacts.

        This will automatically determine if this is an execution or an entity
        and change the type automatically.
        """
        org = _get_organization(self.config.platform)
        if isinstance(entity, Artifact):
            url = f"{self.generate_console_http_domain()}/console/projects/{entity.project}/domains/{entity.domain}/artifacts/{entity.name}/versions/{entity.version}"  # noqa: E501
        else:
            url = super().generate_console_url(entity)
        if org is None:
            return url

        console_http_domain = self.generate_console_http_domain()
        old_prefix = f"{console_http_domain}/console/"
        new_prefix = f"{console_http_domain}/org/{org}/"

        return url.replace(old_prefix, new_prefix)

    @property
    def artifacts_client(self) -> artifacts_pb2_grpc.ArtifactRegistryStub:
        if self._artifacts_client:
            return self._artifacts_client

        self._artifacts_client = artifacts_pb2_grpc.ArtifactRegistryStub(self.client._channel)
        return self._artifacts_client

    def search_artifacts(
        self,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        artifact_key: typing.Optional[art_id.ArtifactKey] = None,
        query: typing.Optional[ArtifactQuery] = None,
        partitions: typing.Optional[Union[Partitions, typing.Dict[str, str]]] = None,
        time_partition: typing.Optional[Union[datetime.datetime, TimePartition]] = None,
        group_by_key: bool = False,
        limit: int = 100,
    ) -> typing.List[Artifact]:
        if limit > 500:
            raise ValueError("Limit cannot exceed 500")

        union_artifacts = []
        next_token = None
        while len(union_artifacts) < limit:
            search_request = construct_search_artifact_request(
                project=project or self.default_project,
                domain=domain or self.default_domain,
                name=name,
                artifact_key=artifact_key,
                query=query,
                partitions=partitions,
                time_partition=time_partition,
                group_by_key=group_by_key,
                limit=100,
                token=next_token,
            )
            search_response = self.artifacts_client.SearchArtifacts(search_request)
            artifact_list = search_response.artifacts
            next_token = search_response.token

            if len(artifact_list) == 0:
                break

            for al in artifact_list:
                ua = Artifact.from_flyte_idl(al)
                # assigned here because the resolver has an implicit dependency on the remote's context
                # can move into artifact if we are okay just using the current context.
                ua.resolver = LiteralsResolver(literals={ua.name: ua.literal}, variable_map=None, ctx=self.context)
                union_artifacts.append(ua)

        return union_artifacts

    def get_artifact(
        self,
        uri: typing.Optional[str] = None,
        artifact_key: typing.Optional[art_id.ArtifactKey] = None,
        artifact_id: typing.Optional[art_id.ArtifactID] = None,
        query: typing.Optional[typing.Union[art_id.ArtifactQuery, ArtifactQuery]] = None,
        get_details: bool = False,
    ) -> typing.Optional[Artifact]:
        """
        Get the specified artifact.

        :param uri: An artifact URI.
        :param artifact_key: An artifact key.
        :param artifact_id: The artifact ID.
        :param query: An artifact query.
        :param get_details: A bool to indicate whether or not to return artifact details.
        :return: The artifact as persisted in the service.
        """
        if query:
            if isinstance(query, ArtifactQuery):
                q = query.to_flyte_idl()
            else:
                q = query
        elif uri:
            q = art_id.ArtifactQuery(uri=uri)
        elif artifact_key:
            q = art_id.ArtifactQuery(artifact_id=art_id.ArtifactID(artifact_key=artifact_key))
        elif artifact_id:
            q = art_id.ArtifactQuery(artifact_id=artifact_id)
        else:
            raise ValueError("One of uri, key, id")
        req = artifacts_pb2.GetArtifactRequest(query=q, details=get_details)
        resp = self.artifacts_client.GetArtifact(req)
        a = Artifact.from_flyte_idl(resp.artifact)
        if a.literal and a.name:
            # assigned here because the resolver has an implicit dependency on the remote's context
            # can move into artifact if we are okay just using the current context.
            a.resolver = LiteralsResolver(literals={a.name: a.literal}, variable_map=None, ctx=self.context)
        return a

    def _execute(
        self,
        entity: typing.Union[FlyteTask, FlyteWorkflow, FlyteLaunchPlan],
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        execution_name: typing.Optional[str] = None,
        execution_name_prefix: typing.Optional[str] = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
        overwrite_cache: typing.Optional[bool] = None,
        envs: typing.Optional[typing.Dict[str, str]] = None,
        tags: typing.Optional[typing.List[str]] = None,
        cluster_pool: typing.Optional[str] = None,
        **kwargs,
    ) -> FlyteWorkflowExecution:
        resolved_inputs = {}
        for k, v in inputs.items():
            # TODO: Remove when https://github.com/flyteorg/flytekit/pull/2136 gets merged
            if Artifact is None:
                resolved_inputs[k] = v
            elif isinstance(v, artifacts_pb2.Artifact):
                lit = v.spec.value
                resolved_inputs[k] = lit
            elif isinstance(v, Artifact):
                if v.literal is not None:
                    lit = v.literal
                elif v.to_id_idl() is not None:
                    fetched_artifact = self.get_artifact(artifact_id=v.concrete_artifact_id)
                    if not fetched_artifact:
                        raise user_exceptions.FlyteValueException(
                            v.concrete_artifact_id, "Could not find artifact with ID given"
                        )
                    lit = fetched_artifact.literal
                else:
                    raise user_exceptions.FlyteValueException(
                        v, "When binding input to Artifact, either the Literal or the ID must be set"
                    )
                resolved_inputs[k] = lit
            else:
                resolved_inputs[k] = v

        return super()._execute(
            entity,
            resolved_inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            execution_name_prefix=execution_name_prefix,
            options=options,
            wait=wait,
            type_hints=type_hints,
            overwrite_cache=overwrite_cache,
            envs=envs,
            tags=tags,
            cluster_pool=cluster_pool,
            **kwargs,
        )

    def create_artifact(self, artifact: Artifact) -> Artifact:
        """
        Create an artifact in FlyteAdmin.

        :param artifact: The artifact to create.
        :return: The artifact as persisted in the service.
        """
        # Two things can happen here -
        #  - the call to to_literal may upload something, in the case of an offloaded data type.
        #    - if this happens, the upload request should already return the created Artifact object.
        if artifact.literal is None:
            with self.remote_context() as ctx:
                lt = artifact.literal_type or TypeEngine.to_literal_type(artifact.python_type)
                lit = TypeEngine.to_literal(ctx, artifact.python_val, artifact.python_type, lt)
                artifact.literal_type = lt.to_flyte_idl()
                artifact.literal = lit.to_flyte_idl()
        else:
            if artifact.literal_type is None:
                raise ValueError("Cannot create an artifact without a literal type set.")

        if artifact.project is None:
            artifact.project = self.default_project
        if artifact.domain is None:
            artifact.domain = self.default_domain
        create_request = Artifact.to_create_request(artifact)
        logging.debug(f"CreateArtifact request {create_request}")
        resp = self.artifacts_client.CreateArtifact(create_request)
        logging.debug(f"CreateArtifact response {resp}")
        return Artifact.from_flyte_idl(resp.artifact)

    def deploy_app(self, app: App, project: Optional[str] = None, domain: Optional[str] = None) -> AppIDL:
        """
        Deploy an application.

        :param app: Application to deploy.
        :param project: Project name. If None, uses default_project.
        :param project: Domain name. If None, uses default_domain.
        :return: The App IDL for the deployed application.
        """
        return self._app_remote.deploy(app, project=project, domain=domain)

    def stop_app(self, name: str, project: Optional[str] = None, domain: Optional[str] = None):
        """
        Stop an application.

        :param name: Name of application to stop.
        :param project: Project name. If None, uses default_project.
        :param project: Domain name. If None, uses default_domain.
        :return: The App IDL for the stopped application.
        """
        return self._app_remote.stop(name=name, project=project, domain=domain)

    def _has_file_extension(self, file_path) -> bool:
        _, ext = os.path.splitext(file_path)
        return bool(ext)

    def get(self, uri: typing.Optional[str] = None) -> typing.Optional[typing.Union[LiteralsResolver, Literal, bytes]]:
        if not uri.startswith("union://"):
            # Assume this is the default behavior and this function is being called with a flyte uri
            return super().get(uri)
        if self._has_file_extension(uri):
            blob_dimensionality = BlobType.BlobDimensionality.SINGLE
        else:
            blob_dimensionality = BlobType.BlobDimensionality.MULTIPART
        return Literal(
            scalar=Scalar(
                blob=Blob(
                    metadata=BlobMetadata(
                        type=BlobType(
                            format="",
                            dimensionality=blob_dimensionality,
                        ),
                    ),
                    uri=uri,
                )
            )
        )

    @property
    def images_client(self) -> image_service_pb2_grpc.ImageServiceStub:
        if self._images_client:
            return self._images_client

        self._images_client = image_service_pb2_grpc.ImageServiceStub(self.client._channel)
        return self._images_client

    def _get_image_fqin(self, name: str) -> str:
        if self.config.platform.endpoint.startswith("localhost"):
            # For sandbox testing, assume that we always want to rebuild
            raise FlyteEntityNotExistException("Running in sandbox")
        image_id = image_definition__pb2.ImageIdentifier(name=name)
        org = _get_organization(self.config.platform, channel=self.client._channel)
        req = image_payload__pb2.GetImageRequest(id=image_id, organization=org)
        resp = self.images_client.GetImage(req)
        return resp.image.fqin

    def _user_info(self) -> UserInfoResponse:
        """
        Query the user info.
        """
        client = IdentityServiceStub(self.client._channel)
        return client.UserInfo(UserInfoRequest())
