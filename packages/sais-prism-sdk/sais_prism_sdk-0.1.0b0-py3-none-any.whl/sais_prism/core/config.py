from pydantic import BaseModel, Extra, validator
from typing import Dict, Any, List, Optional, Union
import os
import yaml
from types import SimpleNamespace


class FoundationConfig(BaseModel):
    experiment_name: str = "default_experiment"


class UnifiedDataAccessConfig(BaseModel):
    enabled: bool = False
    cached: bool = True
    token: Optional[str] = None
    data_access: Dict[str, List[str]] = {}


class MLFlowConfig(BaseModel):
    class ModelRepoConfig(BaseModel):
        model_uri: str = ""
        registered: bool = True
        name: str = "default_model"
        tag: Dict[str, str] = {}
        version: str = "0.1.0"

    enabled: bool = True
    auto_log: bool = True
    system_tracing: bool = True
    model_repo: ModelRepoConfig = ModelRepoConfig()
    metrics: Union[Dict[str, List[str]], List[str]] = {}

    @validator("metrics", pre=True)
    def transform_metrics(cls, v):
        if isinstance(v, list):
            return {"metrics": v}
        return v

    artifacts: Union[Dict[str, List[str]], List[str]] = []
    parameters: Dict[str, Any] = {}


class DynamicConfig(BaseModel):
    class Config:
        extra = Extra.allow


class SAISConfig(DynamicConfig):
    foundation: FoundationConfig = FoundationConfig()
    unified_data_access: UnifiedDataAccessConfig = UnifiedDataAccessConfig()
    ml: MLFlowConfig = MLFlowConfig()


class ConfigManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _convert_namespace_to_dict(self, ns):
        """
        Recursively convert a SimpleNamespace to a dictionary while preserving/converting data types.
        """
        if not isinstance(ns, SimpleNamespace):
            if isinstance(ns, str):
                try:
                    return float(ns)
                except ValueError:
                    return ns
            return ns
        return {key: self._convert_namespace_to_dict(value) for key, value in ns.__dict__.items()}

    def _convert_to_namespace(self, model):
        if isinstance(model, BaseModel):
            namespace = SimpleNamespace()
            for name, value in vars(model).items():
                setattr(namespace, name, self._convert_to_namespace(value))
            return namespace
        elif isinstance(model, dict):
            return SimpleNamespace(**{
                k: self._convert_to_namespace(v) for k, v in model.items()
            })
        elif isinstance(model, list):
            return [self._convert_to_namespace(item) for item in model]
        return model

    def _load_config(self):
        config_path = os.path.join(os.getcwd(), "sais_foundation.yaml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "sais_foundation.yaml not found in project root")

        with open(config_path) as f:
            raw_config = yaml.safe_load(f)

        self.config = self._convert_to_namespace(SAISConfig(**raw_config))

    def get(self, key: str, default=None) -> Any:
        return getattr(self.config, key, default)


class DynamicConfigAccessor:
    def __getattr__(self, name: str) -> Any:
        return ConfigManager().get(name)


config = DynamicConfigAccessor()
