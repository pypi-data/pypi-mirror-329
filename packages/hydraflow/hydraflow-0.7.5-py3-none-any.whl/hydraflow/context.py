"""Provide context managers to log parameters and manage the MLflow run context."""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import mlflow
import mlflow.artifacts
from hydra.core.hydra_config import HydraConfig

from hydraflow.mlflow import log_params
from hydraflow.utils import get_artifact_dir

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mlflow.entities.run import Run

log = logging.getLogger(__name__)


@contextmanager
def log_run(
    config: object | None,
    *,
    synchronous: bool | None = None,
) -> Iterator[None]:
    """Log the parameters from the given configuration object.

    This context manager logs the parameters from the provided configuration object
    using MLflow. It also manages the MLflow run context, ensuring that artifacts
    are logged and the run is properly closed.

    Args:
        config (object): The configuration object to log the parameters from.
        synchronous (bool | None): Whether to log the parameters synchronously.
            Defaults to None.

    Yields:
        None

    Example:
        ```python
        with log_run(config):
            # Perform operations within the MLflow run context
            pass
        ```

    """
    if config:
        log_params(config, synchronous=synchronous)

    hc = HydraConfig.get()
    output_dir = Path(hc.runtime.output_dir)

    # Save '.hydra' config directory.
    output_subdir = output_dir / (hc.output_subdir or "")
    mlflow.log_artifacts(output_subdir.as_posix(), hc.output_subdir)

    try:
        yield

    except Exception as e:
        msg = f"Error during log_run: {e}"
        log.exception(msg)
        raise

    finally:
        log_text(output_dir)


def log_text(directory: Path, pattern: str = "*.log") -> None:
    """Log text files in the given directory as artifacts.

    Append the text files to the existing text file in the artifact directory.

    Args:
        directory (Path): The directory to find the logs in.
        pattern (str): The pattern to match the logs.

    """
    artifact_dir = get_artifact_dir()

    for file in directory.glob(pattern):
        if not file.is_file():
            continue

        file_artifact = artifact_dir / file.name
        if file_artifact.exists():
            text = file_artifact.read_text()
            if not text.endswith("\n"):
                text += "\n"
        else:
            text = ""

        text += file.read_text()
        mlflow.log_text(text, file.name)


@contextmanager
def start_run(  # noqa: PLR0913
    config: object,
    *,
    chdir: bool = False,
    run: Run | None = None,
    run_id: str | None = None,
    experiment_id: str | None = None,
    run_name: str | None = None,
    nested: bool = False,
    parent_run_id: str | None = None,
    tags: dict[str, str] | None = None,
    description: str | None = None,
    log_system_metrics: bool | None = None,
    synchronous: bool | None = None,
) -> Iterator[Run]:
    """Start an MLflow run and log parameters using the provided configuration object.

    This context manager starts an MLflow run and logs parameters using the specified
    configuration object. It ensures that the run is properly closed after completion.

    Args:
        config (object): The configuration object to log parameters from.
        chdir (bool): Whether to change the current working directory to the
            artifact directory of the current run. Defaults to False.
        run (Run | None): The existing run. Defaults to None.
        run_id (str | None): The existing run ID. Defaults to None.
        experiment_id (str | None): The experiment ID. Defaults to None.
        run_name (str | None): The name of the run. Defaults to None.
        nested (bool): Whether to allow nested runs. Defaults to False.
        parent_run_id (str | None): The parent run ID. Defaults to None.
        tags (dict[str, str] | None): Tags to associate with the run. Defaults to None.
        description (str | None): A description of the run. Defaults to None.
        log_system_metrics (bool | None): Whether to log system metrics.
            Defaults to None.
        synchronous (bool | None): Whether to log parameters synchronously.
            Defaults to None.

    Yields:
        Run: An MLflow Run object representing the started run.

    Example:
        with start_run(config) as run:
            # Perform operations within the MLflow run context
            pass

    See Also:
        - `mlflow.start_run`: The MLflow function to start a run directly.
        - `log_run`: A context manager to log parameters and manage the MLflow
           run context.

    """
    if run:
        run_id = run.info.run_id

    with (
        mlflow.start_run(
            run_id=run_id,
            experiment_id=experiment_id,
            run_name=run_name,
            nested=nested,
            parent_run_id=parent_run_id,
            tags=tags,
            description=description,
            log_system_metrics=log_system_metrics,
        ) as run,
        log_run(config if run_id is None else None, synchronous=synchronous),
    ):
        if chdir:
            with chdir_artifact(run):
                yield run
        else:
            yield run


@contextmanager
def chdir_artifact(run: Run | None = None) -> Iterator[Path]:
    """Change the current working directory to the artifact directory of the given run.

    This context manager changes the current working directory to the artifact
    directory of the given run. It ensures that the directory is changed back
    to the original directory after the context is exited.

    Args:
        run (Run | None): The run to get the artifact directory from.

    """
    curdir = Path.cwd()
    artifact_dir = get_artifact_dir(run)

    os.chdir(artifact_dir)

    try:
        yield artifact_dir

    finally:
        os.chdir(curdir)
