import os
import shutil
from pathlib import Path
from typing import List

from frogml_core.exceptions import FrogmlException

DEFAULT_ZIP_NAME = "code"
DEFAULT_ZIP_FORMAT = "zip"
IGNORED_PATTERNS_FOR_UPLOAD = [r"\..*", r"__pycache__"]
HIDDEN_DIRS_TO_INCLUDE = [".dvc"]
HIDDEN_FILES_PREFIX = "."


def _zip_model(
    code_dir_path: str,
    target_dir: str,
    zip_name: str = DEFAULT_ZIP_NAME,
):
    """
    Zip model code directory
    :param code_dir_path:
    :param target_dir: Directory to save the zipped file
    :param zip_name: Name of the zipped file
    :return: return Path object of the zipped file if code_dir_path is not None else None
    """
    if code_dir_path:
        try:
            code_dir_path = os.path.expanduser(code_dir_path)
            dest_dir = os.path.join(target_dir, "filtered_model_files")
            ignored_files = _get_files_to_ignore(directory=Path(code_dir_path))

            shutil.copytree(
                src=code_dir_path,
                dst=dest_dir,
                ignore=shutil.ignore_patterns(*ignored_files),
                dirs_exist_ok=True,
            )

            zip_file_path = os.path.join(target_dir, zip_name)
            zip_path = Path(
                shutil.make_archive(
                    base_name=zip_file_path,
                    format=DEFAULT_ZIP_FORMAT,
                    root_dir=dest_dir,
                )
            )

            shutil.rmtree(dest_dir)

            return zip_path.absolute().as_posix()

        except Exception as e:
            raise FrogmlException(f"Unable to zip model: {e}")
    else:
        return None


def _get_files_to_ignore(directory: Path) -> List[str]:
    def ignore_hidden(file: Path, exclusions: List[str]):
        name = os.path.basename(os.path.abspath(file))
        is_hidden = name.startswith(HIDDEN_FILES_PREFIX) and name not in exclusions
        return is_hidden

    return [
        file.name
        for file in Path(directory).rglob("*")
        if ignore_hidden(file, exclusions=HIDDEN_DIRS_TO_INCLUDE)
    ]


def _get_file_extension(file_path: str) -> str:
    """
    Get file extension
    :param file_path: File path
    :return: File extension
    """
    suffix = Path(file_path).suffix
    if suffix:
        suffix = suffix[1:]
    return suffix


def _get_full_model_path(target_dir: str, model_name: str, serialized_type: str) -> str:
    return os.path.join(target_dir, f"{model_name}.{serialized_type}")
