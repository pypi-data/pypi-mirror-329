from functools import wraps
from .config import ConfigManager
from .exceptions import ConfigurationError
from .service_locator import ServiceLocator
from ..ml.mlflow_integration import initialize
from datetime import datetime
import mlflow


def sais_foundation(cls):
    config = ConfigManager().config

    for section in ["foundation", "unified_data_access", "ml"]:
        if hasattr(config, section):
            setattr(cls, f"_{section}_config", getattr(config, section))

    if not config.foundation.experiment_name:
        raise ConfigurationError(
            "Experiment name is required in foundation config")

    if config.ml.enabled:
        ml = _init_mlflow_integration(cls)
        if hasattr(cls, 'run'):
            original_run = cls.run

            @wraps(original_run)
            def wrapped_run(self, *args, **kwargs):
                version = datetime.now().strftime("%Y%m%d_%H%M%S")
                run_name = f"{cls.__name__}-v{version}"
                with mlflow.start_run(run_name=run_name):
                    try:
                        ml.init_run()
                        result = original_run(self, *args, **kwargs)
                        return result
                    except Exception as e:
                        mlflow_manager.log_params("error", str(e))
                        raise
            cls.run = wrapped_run

    if config.unified_data_access.enabled:
        _init_data_access_client(cls)

    return cls


def _init_mlflow_integration(cls):
    from ..ml import mlflow_integration

    ml_instance = mlflow_integration.initialize(
        experiment_name=cls._foundation_config.experiment_name, config=cls._ml_config, mlflow=mlflow)
    ServiceLocator.set_ml_manager(ml_instance)
    return ml_instance


def _init_data_access_client(cls):
    from ..unified_data_access import client

    data_client = client.initialize(
        **vars(cls._unified_data_access_config)
    )
    ServiceLocator.set_data_client(data_client)
    return data_client
