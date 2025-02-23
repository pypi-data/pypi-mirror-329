import logging
from platform import python_version
from typing import Dict, Optional, List, Callable

from frogml_core.clients.jfrog_gateway import JfrogGatewayClient
from frogml_core.clients.model_version_manager import ModelVersionManagerClient
from frogml_core.utils.proto_utils import ProtoUtils
from frogml_proto.jfml.model_version.v1.model_version_framework_pb2 import (
    ModelVersionFramework,
)
from frogml_proto.qwak.jfrog.gateway.v0.repository_service_pb2 import (
    GetRepositoryConfigurationResponse,
)
from frogml_storage.frog_ml import SerializationMetadata, FrogMLStorage

from frogml.utils.dependencies_tools import _dependency_files_handler
from frogml.utils.files_tools import _zip_model
from frogml.utils.validations import _validate_load_model

_STORAGE_MODEL_ENTITY_TYPE = "model"
_PYTHON_RUNTIME = "python"

_logger = logging.getLogger(__name__)


def _get_model_metadata(
    model_flavor: str,
    model_flavor_version: str,
    serialization_format: str,
) -> SerializationMetadata:
    return SerializationMetadata(
        framework=model_flavor,
        framework_version=model_flavor_version,
        serialization_format=serialization_format,
        runtime=_PYTHON_RUNTIME,
        runtime_version=python_version(),
    )


def _get_model_info_from_artifactory(
    repository: str,
    model_name: str,
    version: str,
) -> Dict:
    return FrogMLStorage().get_entity_manifest(
        entity_type=_STORAGE_MODEL_ENTITY_TYPE,
        repository=repository,
        entity_name=model_name,
        version=version,
        namespace=None,
    )


def _download_model_version_from_artifactory(
    model_flavor: str,
    repository: str,
    model_name: str,
    version: str,
    model_framework: str,
    download_target_path: str,
    deserializer: Callable,
):
    """
    Download model version from artifactory
    :param model_flavor: model flavor files/catboost etc.
    :param repository: repository name
    :param model_name: the name of the model
    :param version: version of the model
    :param download_target_path: the path to download the model to
    :param model_framework: model framework files/catboost etc.
    :return: Loaded model
    """
    _validate_load_model(
        repository=repository,
        model_name=model_name,
        version=version,
        model_framework=model_framework,
        model_flavor=model_flavor,
    )

    FrogMLStorage().download_model_version(
        repository=repository,
        model_name=model_name,
        version=version,
        target_path=download_target_path,
    )
    return deserializer()


def _log_model(
    model_name: str,
    target_dir: str,
    model_flavor: str,
    framework_version: str,
    full_model_path: str,
    serialization_format: str,
    repository: str,
    version: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
    dependencies: Optional[List[str]] = None,
    code_dir: Optional[str] = None,
) -> None:
    project_key: str = __get_project_key(repository)
    model_version_framework: ModelVersionFramework = (
        ProtoUtils.model_framework_from_file_format(
            serialization_format, framework_version
        )
    )

    __validate_model_version(
        project_key, repository, model_name, version, model_version_framework
    )

    __log_model_to_artifactory(
        code_dir,
        dependencies,
        full_model_path,
        model_flavor,
        model_name,
        framework_version,
        properties,
        repository,
        serialization_format,
        target_dir,
        version,
    )

    __create_model_version(
        project_key, repository, model_name, version, model_version_framework
    )


def __get_project_key(repository_key: str) -> str:
    _logger.info("Getting project key for repository %s", repository_key)

    jfrog_gateway_client = JfrogGatewayClient()
    response: GetRepositoryConfigurationResponse = (
        jfrog_gateway_client.get_repository_configuration(repository_key=repository_key)
    )

    if not response.repository_spec or not response.repository_spec.project_key:
        raise ValueError(f"Repository {repository_key} does not belong to any project")

    return response.repository_spec.project_key


def __create_model_version(
    project_key: str,
    repository: str,
    model_name: str,
    model_version: str,
    model_version_framework: ModelVersionFramework,
):
    model_version_manager_client = ModelVersionManagerClient()

    try:
        model_version_manager_client.create_model_version(
            project_key=project_key,
            repository_key=repository,
            model_name=model_name,
            model_version_name=model_version,
            model_version_framework=model_version_framework,
        )
    except Exception as e:
        _logger.warning(
            "Failed to create model version %s in JFML due to this following error: %s\n"
            "Before retrying, please delete the uploaded artifact from Artifactory",
            model_version,
            e,
        )


def __validate_model_version(
    project_key: str,
    repository: str,
    model_name: str,
    model_version: str,
    model_version_framework: ModelVersionFramework,
):
    try:
        model_version_manager_client = ModelVersionManagerClient()
        model_version_manager_client.validate_create_model_version(
            project_key=project_key,
            repository_key=repository,
            model_name=model_name,
            model_version_name=model_version,
            model_version_framework=model_version_framework,
        )
    except Exception as e:
        raise ValueError(str(e)) from e


def __log_model_to_artifactory(
    code_dir,
    dependencies,
    full_model_path,
    model_flavor,
    model_name,
    model_version,
    properties,
    repository,
    serialization_format,
    target_dir,
    version,
):
    dependencies = _dependency_files_handler(
        dependencies=dependencies, target_dir=target_dir
    )
    zipped_code_path = _zip_model(code_dir_path=code_dir, target_dir=target_dir)
    metadata = _get_model_metadata(
        model_flavor=model_flavor,
        model_flavor_version=model_version,
        serialization_format=serialization_format,
    )
    FrogMLStorage().upload_model_version(
        repository=repository,
        model_name=model_name,
        model_path=full_model_path,
        model_type=metadata,
        version=version,
        properties=properties,
        dependencies_files_paths=dependencies,
        code_archive_file_path=zipped_code_path,
    )
