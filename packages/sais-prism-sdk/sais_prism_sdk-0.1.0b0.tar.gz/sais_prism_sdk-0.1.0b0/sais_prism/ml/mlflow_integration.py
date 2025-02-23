from typing import Any, Dict, Optional
import numpy as np
from ..core.config import ConfigManager
from transformers import TrainerCallback


class MLflowManager(TrainerCallback):
    """MLflow integration manager that also acts as a Trainer callback"""

    def __init__(self, experiment_name: str, config: Any, mlflow) -> None:
        self.url = "http://mlflow.internal.sais.com.cn"
        self.experiment_name = experiment_name
        self.ml_config = config
        self.config = ConfigManager()
        self.mlflow = mlflow
        self.mlflow.set_tracking_uri(self.url)
        self.mlflow.set_experiment(experiment_name)
        self.system_tracing(self.ml_config.system_tracing)
        self.mlflow.autolog()

    def init_run(self) -> None:
        """Initialize MLflow run with parameters, model info and artifacts"""
        self.log_params(self.config._convert_namespace_to_dict(
            self.ml_config.parameters))

        self.log_model(self.config._convert_namespace_to_dict(
            self.ml_config.model_repo))

        self.log_artifacts(self.ml_config.artifacts)

    def on_log(self, args, state, control, logs=None, **kwargs):
        """Callback method to log metrics during training"""
        if state.is_world_process_zero and logs is not None:
            for k, v in logs.items():
                if isinstance(v, (int, float)):
                    self.log_metrics({k: v}, step=state.global_step)
#
#    def on_train_end(self, args, state, control, **kwargs):
#        self.mlflow.log_artifacts(self.config.artifacts_dir)

    def system_tracing(self, enabled: bool) -> None:
        """Enable or disable system metrics logging"""
        if enabled:
            self.mlflow.enable_system_metrics_logging()
            print("System Metrics is Enabled")
        else:
            print("System Metrics is Disabled")

    def log_model(self, params: Dict[str, Any]) -> None:
        """Log model information to MLflow"""
        if not params:
            return

        required_fields = {"model_uri", "name", "version"}
        if missing := required_fields - params.keys():
            raise ValueError(f"Missing required fields: {missing}")

        model_uri = params["model_uri"].format(
            run_id=self.mlflow.active_run().info.run_id)

        self.mlflow.register_model(
            model_uri=model_uri,
            name=params["name"],
            tags={
                "version": params["version"],
                **params.get("tag", {})
            }
        )

    def log_params(self, params: Dict[str, Any]) -> None:
        """Log parameters to MLflow"""
        if params:
            self.mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: int = 0) -> None:
        """Log metrics to MLflow with optional step number"""
        if metrics:
            self.mlflow.log_metrics(metrics, step=step)

    def log_artifacts(self, artifacts: Dict[str, Any]) -> None:
        """Log artifacts to MLflow"""
        if artifacts:
            if isinstance(artifacts, list):
                artifacts = {"artifacts": artifacts}
            for artifact in artifacts.values():
                self.mlflow.log_artifacts(artifact)

    def set_log_artifacts(self, obj_str: str) -> None:
        """Log a single artifact to MLflow"""
        if obj_str:
            self.mlflow.log_artifacts(obj_str)

    def set_log_params(self, key: str, val: str) -> None:
        """Log a single parameter to MLflow"""
        if key and val:
            self.mlflow.log_param(key, val)

    def _ml_termination_(self) -> None:
        """End the current MLflow run"""
        if self.mlflow.active_run():
            self.mlflow.end_run()


def initialize(experiment_name: str, config: Any, mlflow: Any) -> MLflowManager:
    """Initialize and return a new MLflowManager instance"""
    global client
    client = MLflowManager(experiment_name, config, mlflow)
    return client
