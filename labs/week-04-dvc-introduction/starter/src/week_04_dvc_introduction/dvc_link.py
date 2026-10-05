"""Record the DVC data version on the MLflow run (Exercises 6 and 7)."""

from __future__ import annotations

import mlflow

from .config import Settings
from .datasets import file_md5
from .dvc_meta import pointer_md5, remote_object_uri


def dvc_data_url(settings: Settings) -> str:
    """The s3:// URI of the current data version in the DVC remote.

    Uses `dvc.api.get_url`, or builds the same URI from the pointer's md5 when
    the file is outside a DVC project.
    """
    try:
        import dvc.api

        return str(dvc.api.get_url(str(settings.measurements_path)))
    except Exception:
        return remote_object_uri(settings, pointer_md5(settings.measurements_path))


def log_data_version(settings: Settings) -> dict:
    """Tag the active run with the data version. Returns what was logged."""
    tags = {
        "dvc_md5": pointer_md5(settings.measurements_path),
        "dvc_url": dvc_data_url(settings),
        "dvc_remote": f"{settings.dvc_bucket}/{settings.dvc_remote_path}",
        "data_file": settings.measurements_path.name,
    }
    mlflow.set_tags(tags)
    return tags


def log_dataset_input(frame, settings: Settings, source: str) -> str | None:
    """Log the training data as an MLflow Dataset input. Returns its digest."""
    from .data import TARGET_COLUMN
    
    dataset = mlflow.data.from_pandas(
        frame, 
        name="diabetes-measurements", 
        targets=TARGET_COLUMN,
        source=source
    )
    mlflow.log_input(dataset, context="training")
    return dataset.digest


def require_data_added(settings: Settings) -> str:
    """Check that the data on disk is the data the pointer names. Returns its md5.

    TODO(student) — Exercise 7 (optional): compare the md5 of the file on disk
    (file_md5) with the md5 in its pointer (pointer_md5). If they differ, raise a
    RuntimeError whose message tells the user to run `dvc add`.
    """
    _ = file_md5  # keep the import meaningful until you implement the body
    return ""  # placeholder: no check yet
