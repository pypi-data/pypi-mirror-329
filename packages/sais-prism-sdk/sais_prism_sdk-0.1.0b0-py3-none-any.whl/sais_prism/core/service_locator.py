from typing import Optional
from sais_prism.ml.mlflow_integration import MLflowManager
from sais_prism.unified_data_access.client import DataAccessClient


class ServiceLocator:
    _ml_instance: Optional[MLflowManager] = None
    _data_client_instance: Optional[DataAccessClient] = None

    @classmethod
    def get_ml_manager(cls) -> MLflowManager:
        if cls._ml_instance is None:
            raise RuntimeError("MLflowManager not initialized")
        return cls._ml_instance

    @classmethod
    def set_ml_manager(cls, instance: MLflowManager):
        cls._ml_instance = instance

    @classmethod
    def get_data_client(cls) -> DataAccessClient:
        if cls._data_client_instance is None:
            raise RuntimeError("DataAccessClient not initialized")
        return cls._data_client_instance

    @classmethod
    def set_data_client(cls, instance: DataAccessClient):
        cls._data_client_instance = instance
