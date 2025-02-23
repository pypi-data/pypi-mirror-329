import logging
import os.path
import tempfile
from functools import partial
from typing import Dict, List, Optional

from frogml_core.exceptions import FrogmlException
from frogml_core.utils.proto_utils import HUGGINGFACE_FRAMEWORK_FORMAT

from frogml.utils.files_tools import _get_full_model_path
from frogml.utils.storage import (
    _log_model,
    _get_model_info_from_artifactory,
    _download_model_version_from_artifactory,
)
from frogml.utils.storage_helper import (
    _get_model_framework,
    _get_model_framework_version,
)
from frogml.utils.validations import _validate_typed_log_model, _validate_load_model

_logger = logging.getLogger(__name__)
_HUGGINGFACE_LEARN_MODEL_FLAVOR = "huggingface"


def log_model(
    model,
    tokenizer,
    model_name: str,
    repository: str,
    version: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
    dependencies: Optional[List[str]] = None,
    code_dir: Optional[str] = None,
) -> None:
    """
    Log Hugging face model to Artifactory
    :param model: Model to log
    :param tokenizer: Tokenizer to log
    :param model_name: Name of the model
    :param repository: Repository to log the model to
    :param version: Version of the model
    :param properties: Model properties
    :param dependencies: Model dependencies
    :param code_dir: Directory containing the code
    :return:
    """
    _logger.info(f"Logging model {model_name} to {repository}")
    _validate_typed_log_model(
        repository=repository,
        model_name=model_name,
        version=version,
        properties=properties,
        dependencies=dependencies,
        code_dir=code_dir,
    )

    with tempfile.TemporaryDirectory() as target_dir:
        full_model_path = _get_full_model_path(
            target_dir=target_dir,
            model_name=model_name,
            serialized_type=HUGGINGFACE_FRAMEWORK_FORMAT,
        )

        model.save_pretrained(full_model_path)
        tokenizer.save_pretrained(full_model_path)

        try:
            import transformers

            model_version = transformers.__version__
        except Exception as e:
            raise FrogmlException(f"Failed to get transformers version: {e}")

        _log_model(
            model_name=model_name,
            target_dir=target_dir,
            model_flavor=_HUGGINGFACE_LEARN_MODEL_FLAVOR,
            framework_version=model_version,
            full_model_path=full_model_path,
            serialization_format=HUGGINGFACE_FRAMEWORK_FORMAT,
            repository=repository,
            version=version,
            properties=properties,
            dependencies=dependencies,
            code_dir=code_dir,
        )


def get_model_info(repository: str, model_name: str, version: str) -> Dict:
    """
    Get model information
    :param repository:
    :param model_name:
    :param version:
    :return: Model information
    """

    _logger.info(f"Getting model {model_name} information from {repository}")

    return _get_model_info_from_artifactory(
        repository=repository,
        model_name=model_name,
        version=version,
    )


def load_model(repository: str, model_name: str, version: str):
    """
    Load model from Artifactory.
    :param repository: Repository to load the model from
    :param model_name: Name of the model
    :param version: Version of the model
    :return: tuple of Model and tokenizer
    """

    _logger.info(f"Loading model {model_name} from {repository}")

    with tempfile.TemporaryDirectory() as download_target_path:

        model_info = get_model_info(
            repository=repository, model_name=model_name, version=version
        )
        model_framework = _get_model_framework(model_info)
        framework_runtime_version = _get_model_framework_version(model_info)

        _validate_load_model(
            repository=repository,
            model_name=model_name,
            version=version,
            model_framework=model_framework,
            model_flavor=_HUGGINGFACE_LEARN_MODEL_FLAVOR,
        )

        full_model_path = os.path.join(download_target_path, f"{model_name}")

        def deserializer_model(model_path):
            from transformers import DistilBertModel, DistilBertTokenizer

            model = DistilBertModel.from_pretrained(model_path)
            tokenizer = DistilBertTokenizer.from_pretrained(model_path)

            return model, tokenizer

        try:
            return _download_model_version_from_artifactory(
                model_flavor=_HUGGINGFACE_LEARN_MODEL_FLAVOR,
                repository=repository,
                model_name=model_name,
                version=version,
                model_framework=model_framework,
                download_target_path=full_model_path,
                deserializer=partial(deserializer_model, full_model_path),
            )
        except Exception as e:

            logging.error(
                f"Failed to load Model. Model was serialized with transformers using DistilBert version: {framework_runtime_version}"
            )
            raise FrogmlException(f"Failed to deserialized model: {e}")
