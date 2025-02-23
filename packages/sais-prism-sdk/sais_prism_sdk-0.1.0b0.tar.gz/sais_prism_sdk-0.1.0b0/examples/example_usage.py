"""Example usage of SAIS Prism for ML experiment tracking"""

from sais_prism.core.decorators import sais_foundation
from sais_prism.core.config import config
from sais_prism.core.service_locator import ServiceLocator


@sais_foundation
class Example:
    def run(self):
        if config.unified_data_access.enabled:
            print(
                "Accessing dataset:",
                config.unified_data_access.data_access[0]["dataset_names"],
            )
            # ServiceLocator.get_ml_manager().log_metrics()
        if config.ml.enabled:
            print(f"Training {config.ml.model_repo.name}")


if __name__ == "__main__":
    app = Example()
    app.run()
