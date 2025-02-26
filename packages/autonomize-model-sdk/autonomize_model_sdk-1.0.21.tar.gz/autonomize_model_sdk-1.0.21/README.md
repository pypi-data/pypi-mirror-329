# ModelHub SDK

ModelHub SDK is a powerful tool for orchestrating and managing machine learning workflows, experiments, datasets, and deployments on Kubernetes. It integrates seamlessly with MLflow and supports custom pipelines, dataset management, model logging, and serving through Kserve.

![Python Version](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![PyPI Version](https://img.shields.io/pypi/v/autonomize-model-sdk?style=for-the-badge&logo=pypi)
![Code Formatter](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)
![Code Linter](https://img.shields.io/badge/linting-pylint-green.svg?style=for-the-badge)
![Code Checker](https://img.shields.io/badge/mypy-checked-blue?style=for-the-badge)
![Code Coverage](https://img.shields.io/badge/coverage-96%25-a4a523?style=for-the-badge&logo=codecov)

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Quickstart](#quickstart)
4. [CLI Tool](#cli-tool)
5. [Experiments and Runs](#experiments-and-runs)
   - [Logging Parameters and Metrics](#logging-parameters-and-metrics)
   - [Artifact Management](#artifact-management)
6. [Pipeline Management](#pipeline-management)
   - [Pipeline Definition](#pipeline-definition)
   - [Running a Pipeline](#running-a-pipeline)
7. [Dataset Management](#dataset-management)
   - [Loading Datasets](#loading-datasets)
8. [Model Deployment through Kserve](#model-deployment-through-kserve)
9. [Examples](#examples)

## Installation

To install the ModelHub SDK, simply run:

```bash
pip install autonomize-model-sdk
```

## Environment Setup
Ensure you have the following environment variables set in your system:

```bash
export MODELHUB_BASE_URL=https://api-modelhub.example.com
export MODELHUB_CLIENT_ID=your_client_id
export MODELHUB_CLIENT_SECRET=your_client_secret
export MLFLOW_EXPERIMENT_ID=your_experiment_id
```

Alternatively, create a .env file in your project directory and add the above environment variables.

## CLI Tool

The ModelHub SDK includes a command-line interface for managing ML pipelines:

```bash
# Start a pipeline in local mode (with local scripts)
pipeline start -f pipeline.yaml --mode local --pyproject pyproject.toml

# Start a pipeline in CI/CD mode (using container)
pipeline start -f pipeline.yaml --mode cicd
```

CLI Options:
- `-f, --file`: Path to pipeline YAML file (default: pipeline.yaml)
- `--mode`: Execution mode ('local' or 'cicd')
  - local: Runs with local scripts and installs dependencies using Poetry
  - cicd: Uses container image with pre-installed dependencies
- `--pyproject`: Path to pyproject.toml file (required for local mode)

## Quickstart
The ModelHub SDK allows you to easily log experiments, manage pipelines, and use datasets.

Here's a quick example of how to initialize the client and log a run:

```python
import os
from modelhub.clients import MLflowClient

# Initialize the ModelHub client
client = MLflowClient(base_url=os.getenv("MODELHUB_BASE_URL"))
experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID")

client.set_experiment(experiment_id=experiment_id)

# Start an MLflow run
with client.start_run(run_name="my_experiment_run"):
    client.mlflow.log_param("param1", "value1")
    client.mlflow.log_metric("accuracy", 0.85)
    client.mlflow.log_artifact("model.pkl")
```

## Experiments and Runs
ModelHub SDK provides an easy way to interact with MLflow for managing experiments and runs.

### Logging Parameters and Metrics
To log parameters, metrics, and artifacts:

```python
with client.start_run(run_name="my_run"):
    # Log parameters
    client.mlflow.log_param("learning_rate", 0.01)

    # Log metrics
    client.mlflow.log_metric("accuracy", 0.92)
    client.mlflow.log_metric("precision", 0.88)

    # Log artifacts
    client.mlflow.log_artifact("/path/to/model.pkl")
```

### Artifact Management
You can log or download artifacts with ease:

```python
# Log artifact
client.mlflow.log_artifact("/path/to/file.csv")

# Download artifact
client.mlflow.artifacts.download_artifacts(run_id="run_id_here", artifact_path="artifact.csv", dst_path="/tmp")
```

## Pipeline Management
ModelHub SDK enables users to define, manage, and run multi-stage pipelines that automate your machine learning workflow. You can define pipelines in YAML and submit them using the SDK.

### Basic Pipeline
Here's a simple pipeline example:

```yaml
name: "Simple Pipeline"
description: "Basic ML pipeline"
experiment_id: "123"
image_tag: "my-image:1.0.0"
stages:
  - name: train
    type: custom
    script: scripts/train.py
```

### Running a Pipeline
Using CLI:
```bash
# Local development
pipeline start -f pipeline.yaml --mode local --pyproject pyproject.toml

# CI/CD environment
pipeline start -f pipeline.yaml --mode cicd
```

Using SDK:
```python
from modelhub.clients import PipelineManager

pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")
```

### Advanced Configuration
For detailed information about pipeline configuration including:
- Resource management (CPU, Memory, GPU)
- Node scheduling with selectors and tolerations
- Blob storage integration
- Stage dependencies
- Advanced examples and best practices

See our [Pipeline Configuration Guide](./PIPELINE.md).

## Dataset Management
ModelHub SDK allows you to load and manage datasets easily, with support for loading data from external storage or datasets managed through the frontend.

### Loading Datasets
To load datasets using the SDK:

```python
from modelhub import load_dataset

# Load a dataset by name
dataset = load_dataset("my_dataset")

# Load a dataset from a specific directory
dataset = load_dataset("my_dataset", directory="data_folder/")

# Load a specific version and split
dataset = load_dataset("my_dataset", version=2, split="train")

```

### Using Blob Storage for Dataset
```python
# Load dataset from blob storage
dataset = load_dataset(
    "my_dataset",
    blob_storage_config={
        "container": "data",
        "blob_url": "https://storage.blob.core.windows.net",
        "mount_path": "/data"
    }
)

```

## Model Deployment through KServe
Deploy models via KServe after logging them with MLflow:

### Create a model wrapper:
Use the MLflow PythonModel interface to define your model's prediction logic.

```python
import mlflow.pyfunc
import joblib

class ModelWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load("/path/to/model.pkl")

    def predict(self, context, model_input):
        return self.model.predict(model_input)

# Log the model
client.mlflow.pyfunc.log_model(
    artifact_path="model",
    python_model=ModelWrapper()
)
```

### Serve models with ModelHub:

ModelHub SDK provides classes for serving models through KServe:

```python
from modelhub.serving import ModelhubModelService, ModelServer

# Create model service
model_service = ModelhubModelService(
    name="my-classifier",
    run_uri="runs:/abc123def456/model",
    model_type="pyfunc"
)

# Load the model
model_service.load()

# Start the server
ModelServer().start([model_service])
```

ModelHub supports multiple model types including text, tabular data, and image processing. For comprehensive documentation on model serving capabilities, see our [Model Serving Guide](./SERVING.md).

### Deploy with KServe:
After logging the model, deploy it using KServe:

```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "model-service"
  namespace: "modelhub"
  labels:
    azure.workload.identity/use: "true"
spec:
  predictor:
    containers:
      - image: your-registry.io/model-serve:latest
        name: model-service
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        command: [
          "sh", "-c",
          "python app/main.py --model_name my-classifier --run runs:/abc123def456/model"
        ]
        env:
          - name: MODELHUB_BASE_URL
            value: "https://api-modelhub.example.com"
    serviceAccountName: "service-account-name"
```

## Examples

### Training Pipeline with Multiple Stages

```python
from modelhub.clients import MLflowClient, PipelineManager

# Setup clients
mlflow_client = MLflowClient()
pipeline_manager = PipelineManager()

# Define and run pipeline
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")

# Track experiment in MLflow
with mlflow_client.start_run(run_name="Training Run"):
    # Log training parameters
    mlflow_client.log_param("model_type", "transformer")
    mlflow_client.log_param("epochs", 10)

    # Log metrics
    mlflow_client.log_metric("train_loss", 0.123)
    mlflow_client.log_metric("val_accuracy", 0.945)

    # Log model artifacts
    mlflow_client.log_artifact("model.pkl")

```

### Dataset Version Management

```python
from modelhub.clients import DatasetClient

# Initialize client
dataset_client = DatasetClient()

# List available datasets
datasets = dataset_client.list_datasets()

# Get specific version
dataset_v2 = dataset_client.get_dataset_versions("dataset_id")

# Load dataset with version control
dataset = dataset_client.load_dataset(
    "my_dataset",
    version=2,
    split="train"
)

```

## Feedback & Contributions

We welcome contributions to the ModelHub SDK! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows our style guidelines and includes appropriate tests.

For feedback or support:
- Open an issue on GitHub
- Contact the ModelHub team directly
- Check our documentation for updates

## License

Copyright (C) Autonomize AI - All Rights Reserved

The contents of this repository cannot be copied and/or distributed without the explicit permission from Autonomize.ai
