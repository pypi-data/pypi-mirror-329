from platform import python_version

from dependency_injector.wiring import Provide
from grpc import RpcError

from frogml_core.utils.model_utils import get_model_id_from_model_name
from frogml_proto.jfml.model_version.v1.model_repository_spec_pb2 import (
    ModelRepositorySpec,
)
from frogml_proto.jfml.model_version.v1.model_version_framework_pb2 import (
    ModelVersionFramework,
)
from frogml_proto.jfml.model_version.v1.model_version_manager_service_pb2 import (
    CreateModelVersionRequest,
    CreateModelVersionResponse,
)
from frogml_proto.jfml.model_version.v1.model_version_manager_service_pb2_grpc import (
    ModelVersionManagerServiceStub,
)
from frogml_proto.jfml.model_version.v1.model_version_pb2 import ModelVersionSpec
from frogml_core.exceptions import FrogmlException
from frogml_core.inner.di_configuration import FrogmlContainer


class ModelVersionManagerClient:
    """
    Used for interacting with the model version manager's endpoints
    """

    def __init__(self, grpc_channel=Provide[FrogmlContainer.core_grpc_channel]):
        self.__model_version_manager_stub = ModelVersionManagerServiceStub(grpc_channel)

    @staticmethod
    def __build_create_model_version_request(
        project_key: str,
        repository_key: str,
        model_name: str,
        model_version_name: str,
        model_version_framework: ModelVersionFramework,
        dry_run: bool,
    ) -> CreateModelVersionRequest:
        return CreateModelVersionRequest(
            dry_run=dry_run,
            model_version=ModelVersionSpec(
                repository_spec=ModelRepositorySpec(
                    project_key=project_key,
                    repository_key=repository_key,
                    model_id=get_model_id_from_model_name(model_name),
                    model_name=model_name,
                ),
                name=model_version_name,
                framework=model_version_framework,
                python_version=python_version(),
            ),
        )

    def validate_create_model_version(
        self,
        project_key: str,
        repository_key: str,
        model_name: str,
        model_version_name: str,
        model_version_framework: ModelVersionFramework,
    ):
        try:
            create_model_request = self.__build_create_model_version_request(
                project_key=project_key,
                repository_key=repository_key,
                model_name=model_name,
                model_version_name=model_version_name,
                model_version_framework=model_version_framework,
                dry_run=True,
            )
            self.__model_version_manager_stub.CreateModelVersion(create_model_request)
        except RpcError as e:
            message = f"Failed to validate model version, details [{e.details()}]"
            raise FrogmlException(message)

        except Exception as e:
            message = f"Failed to validate model version, details [{e}]"
            raise FrogmlException(message)

    def create_model_version(
        self,
        project_key: str,
        repository_key: str,
        model_name: str,
        model_version_name: str,
        model_version_framework: ModelVersionFramework,
    ) -> CreateModelVersionResponse:
        try:
            create_model_request = self.__build_create_model_version_request(
                project_key=project_key,
                repository_key=repository_key,
                model_name=model_name,
                model_version_name=model_version_name,
                model_version_framework=model_version_framework,
                dry_run=False,
            )
            create_model_version_response: CreateModelVersionResponse = (
                self.__model_version_manager_stub.CreateModelVersion(
                    create_model_request
                )
            )

            return create_model_version_response
        except RpcError as e:
            message = f"Failed to validate model version, details [{e.details()}]"
            raise FrogmlException(message)

        except Exception as e:
            message = f"Failed to validate model version, details [{e}]"
            raise FrogmlException(message)
