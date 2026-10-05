"""The model registry: versions, aliases, governance tags, and traceability.

New in Week 3. Tracking answers "which run scored best?". It cannot answer
"what are we serving?" — for that you need a NAME, a stable address, an approval
record, and a rollback target. That is the registry.

Four nouns:
  registered model  a name, e.g. "diabetes-classifier"
  version           an immutable, numbered snapshot of one run's model
  alias             a MUTABLE pointer to exactly one version: models:/<name>@staging
  tag               a recorded fact attached to a version (who promoted it, on what)

Note what is absent: model *stages*. MLflow deprecated the fixed
None/Staging/Production/Archived state machine in 2.9 and the official registry
tutorial now uses aliases exclusively. See the lab README for the one-line
deviation note, and the lecture for why the change was an improvement.
"""

from __future__ import annotations

from datetime import datetime, timezone

import mlflow
import mlflow.sklearn
from mlflow.entities.model_registry import ModelVersion
from mlflow.tracking import MlflowClient

from .config import Settings

def register_best_model(settings: Settings, run_id: str) -> ModelVersion | None:
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    return mlflow.register_model(
        model_uri=f"runs:/{run_id}/model",
        name=settings.registered_model_name,
        tags={"registered_from": "week3-sweep"}
    )

def latest_version(settings: Settings) -> ModelVersion:
    client = MlflowClient(settings.mlflow_tracking_uri)
    versions = client.search_model_versions(
        f"name = '{settings.registered_model_name}'"
    )
    if not versions:
        raise RuntimeError(
            f"No versions registered under '{settings.registered_model_name}'. "
            "Run 'make register' first (Exercise 5)."
        )
    return max(versions, key=lambda v: int(v.version))

def promote_to_staging(
    settings: Settings, version: str, reason: str | None = None
) -> ModelVersion | None:
    client = MlflowClient(settings.mlflow_tracking_uri)
    name = settings.registered_model_name

    mv = client.get_model_version(name, version)
    run = client.get_run(mv.run_id)

    f1 = run.data.metrics.get('f1', 0.0)
    roc_auc = run.data.metrics.get('roc_auc', 0.0)
    
    client.set_model_version_tag(name, version, "validation_f1", f"{f1:.4f}")
    client.set_model_version_tag(name, version, "validation_roc_auc", f"{roc_auc:.4f}")
    client.set_model_version_tag(name, version, "promoted_by", settings.model_owner)
    client.set_model_version_tag(name, version, "promoted_at", datetime.now(timezone.utc).isoformat(timespec='seconds'))
    if reason:
        client.set_model_version_tag(name, version, "promotion_reason", reason)

    client.set_registered_model_tag(name, "owner", settings.model_owner)
    client.set_registered_model_tag(name, "task", "diabetes-binary-classification")

    client.set_registered_model_alias(name, settings.model_alias, version)
    client.set_registered_model_alias(name, "champion", version)

    return client.get_model_version_by_alias(name, settings.model_alias)

def trace_alias(settings: Settings) -> dict:
    client = MlflowClient(settings.mlflow_tracking_uri)
    name, alias = settings.registered_model_name, settings.model_alias

    mv = client.get_model_version_by_alias(name, alias)

    if not mv.run_id:
        raise RuntimeError("The version has no source run_id.")
    
    run = client.get_run(mv.run_id)

    return {
        "model_uri": f"models:/{name}@{alias}",
        "version": mv.version,
        "aliases": mv.aliases,
        "run_id": mv.run_id,
        "run_name": run.data.tags.get("mlflow.runName"),
        "git_commit": run.data.tags.get("git_commit"),
        "git_dirty": run.data.tags.get("git_dirty"),
        "params": run.data.params,
        "metrics": run.data.metrics,
        "version_tags": mv.tags,
    }

def roll_back(
    settings: Settings, to_version: str, reason: str
) -> tuple[str, ModelVersion] | None:
    client = MlflowClient(settings.mlflow_tracking_uri)
    name = settings.registered_model_name

    current_mv = client.get_model_version_by_alias(name, settings.model_alias)
    current_version = current_mv.version

    if current_version == to_version:
        raise ValueError(f"Alias already points to version {to_version}")
    
    target_mv = client.get_model_version(name, to_version)
    if "promoted_at" not in target_mv.tags:
        raise ValueError(f"Version {to_version} was never promoted.")

    client.set_model_version_tag(name, current_version, "rolled_back_at", datetime.now(timezone.utc).isoformat(timespec='seconds'))
    client.set_model_version_tag(name, current_version, "rolled_back_to", to_version)
    client.set_model_version_tag(name, current_version, "rollback_reason", reason)

    client.set_registered_model_alias(name, settings.model_alias, to_version)
    client.set_registered_model_alias(name, "champion", to_version)

    return (current_version, client.get_model_version_by_alias(name, settings.model_alias))

def load_aliased_model(settings: Settings):
    """Load the model the alias currently points at.

    Two things worth noticing. First, the URI names a ROLE, not a version — the
    caller never changes when the champion changes. Second, this download goes
    through the tracking server's artifact proxy, so the client needs no Silo
    credentials at all. Check your `.env`: there are no AWS_* variables in it.
    """
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    return mlflow.sklearn.load_model(
        f"models:/{settings.registered_model_name}@{settings.model_alias}"
    )