# SAIS Prism SDK

[![PyPI version](https://img.shields.io/pypi/v/sais-prism-sdk)](https://pypi.org/project/sais-prism-sdk/)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

## Unified Interface for ML Lifecycle Management

### Features

- 🚀 Centralized Configuration Management
- 🔄 Auto MLflow Integration
- 📦 Extensible Data Access Layer
- 🧩 Declarative Experiment Tracking
- 📚 Hierarchical Dependency Management

### Installation

```bash
pip install sais-prism-sdk
```

### Configuration
Create `sais_foundation.yaml`:

```yaml
ml:
  model_repo:
    name: "production"
    version: "1.0.0"
    tags:
      framework: "pytorch"

data_access:
  enabled: true
  token: ${ENV_TOKEN}
```

### User Manual

#### Experiment Tracking
```python
@sais_foundation(auto_log=True)
def train(data):
    # Auto-log params/metrics
    accuracy = model.fit()
    return {"accuracy": accuracy}
```

#### Model Deployment
```bash
sais-prism deploy --model-uri models:/prod/1 --env kubernetes
```

#### Data Access
```python
client = DataClient()
data = client.load("mysql.sales_data")
```

### API Reference

| Class | Description |
|-------|-------------|
| `ConfigManager` | Central config access |
| `MLflowService` | Model registry & tracking |
| `DataClient` | Unified data interface |

### Contributing

1. Install dev deps:
```bash
pip install -r requirements/dev.txt
```
2. Run checks:
```bash
black . && flake8
```

## License
[The Unlicense](https://unlicense.org)

## Architecture Design

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=SAIS+Prism+Architecture)

### Core Components

- `ConfigManager`: Centralized configuration management
- `MLflowService`: Model registry and tracking
- `DataClient`: Unified data access interface

### Service Locator

```python
class ServiceLocator:
    _ml_instance: Optional[MLflowManager] = None
    _data_client_instance: Optional[DataAccessClient] = None

    @classmethod
    def get_ml_manager(cls) -> MLflowManager:
        if not cls._ml_instance:
            cls._ml_instance = MLflowManager(config.ml)
        return cls._ml_instance
```

### MLflow Configuration

```yaml
ml:
  enabled: true  # Global switch
  auto_log: true  # Auto-log params/metrics
  model_repo:
    name: "production_models"
    version: "1.0.0"  # Semver required
    tags:  # Custom metadata
      framework: "pytorch"
      task_type: "classification"
  metrics:  # Metric collection config
    training: ["accuracy", "f1_score"]
    validation: ["auc_roc"]
```

### Data Access Configuration

```yaml
data_access:
  enabled: true
  cached: true  # Enable local caching
  token: ${ENV_API_TOKEN}  # Env var injection
  data_access:
    mysql:
      - "sensor_data"
      - "user_behavior"
    mongodb:
      - "log_records"
```

### Advanced Usage

#### Custom Model Tags

```python
# Extend ModelRepoConfig to add custom tags
class CustomModelConfig(ModelRepoConfig):
    deployment_env: str = "staging"
    business_unit: str = "recommendation"

# Specify custom class in config
ml:
  model_repo:
    __class__: "module.path.CustomModelConfig"
    deployment_env: "production"
```

#### Extending Data Clients

1. Implement base client interface:
```python
class CustomDataClient(DataAccessClient):
    def connect(self, config):
        # Init logic

    @retry_policy(max_retries=3)
    def fetch_data(self, source):
        # Data fetch implementation
```
2. Register with service locator:
```python
ServiceLocator.set_data_client(CustomDataClient())
```

### Troubleshooting

#### Config Load Failure
**Symptoms**: `ConfigurationError: sais_foundation.yaml not found`

✅ Solution:
```bash
# Generate default config file
python -m sais_prism.config generate > sais_foundation.yaml
```

#### MLflow Connection Issues
**Symptoms**: `MLFlowIntegrationError: Failed to connect tracking server`

✅ Check steps:
1. Verify MLflow server address
2. Check network connectivity
3. Verify server certificate (if HTTPS enabled)

```python
# Manual connection test
from mlflow.tracking import MlflowClient
client = MlflowClient(config.ml.tracking_uri)
print(client.search_experiments())