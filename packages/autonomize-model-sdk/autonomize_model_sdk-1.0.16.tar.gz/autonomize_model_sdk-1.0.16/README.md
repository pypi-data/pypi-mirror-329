
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
4. [Experiments and Runs](#experiments-and-runs)
    - [Logging Parameters and Metrics](#logging-parameters-and-metrics)
    - [Artifact Management](#artifact-management)
5. [Pipeline Management](#pipeline-management)
    - [Pipeline Definition](#pipeline-definition)
    - [Running a Pipeline](#running-a-pipeline)
6. [Dataset Management](#dataset-management)
    - [Loading Datasets](#loading-datasets)
7. [Model Deployment through Kserve](#model-deployment-through-kserve)
8. [Examples](#examples)

---

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

## Quickstart
The ModelHub SDK allows you to easily log experiments, manage pipelines, and use datasets.

Here’s a quick example of how to initialize the client and log a run:

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

## Logging Parameters and Metrics
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

## Artifact Management
You can log or download artifacts with ease:

```python
# Log artifact
client.mlflow.log_artifact("/path/to/file.csv")

# Download artifact
client.mlflow.artifacts.download_artifacts(run_id="run_id_here", artifact_path="artifact.csv", dst_path="/tmp")
```

## Pipeline Management
ModelHub SDK enables users to define, manage, and run multi-stage pipelines that automate your machine learning workflow. You can define pipelines in YAML and submit them using the SDK.

## Pipeline Definition
Here’s a sample pipeline.yaml file:

```yaml
name: "ModelHub Pipeline Example"
description: "Pipeline with preprocess, training, and evaluation stages"
experiment_id: "9"
dataset_name: "dataset_name"
image_tag: "base-llm:1.0.1"
stages:
  - name: preprocess
    type: custom
    params:
      data_path: "data"
      output_path: "output"
    script: stages/preprocess.py
    requirements: requirements.txt
    resources:
      cpu: "1"
      memory: "1Gi"

  - name: train
    type: custom
    params:
      data_path: "output/train_preprocessed.csv"
      model_path: "output/model"
    script: stages/train.py
    requirements: requirements.txt
    resources:
      cpu: "1"
      memory: "1Gi"

  - name: evaluate
    type: custom
    params:
      model_path: "output/model"
      eval_output_path: "output/eval"
    script: stages/evaluate.py
    requirements: requirements.txt
    resources:
      cpu: "1"
      memory: "1Gi"
```

## Running a Pipeline
To submit and run a pipeline, use the PipelineManager from the SDK:

```python
from modelhub.clients import PipelineManager

pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))

# Start the pipeline
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")
print("Pipeline started:", pipeline)
```

## Dataset Management
ModelHub SDK allows you to load and manage datasets easily, with support for loading data from external storage or datasets managed through the frontend.

## Loading Datasets
To load datasets using the SDK:

```python
from modelhub import load_dataset

# Load a dataset by name
dataset = load_dataset("my_dataset")

# Load a dataset from a specific directory
dataset = load_dataset("my_dataset", directory="data_folder/")
```


## Model Deployment through Kserve
Deploy models via Kserve after logging them with MLflow:

## Create a model wrapper:
Use the MLflow PythonModel interface to define your model's prediction logic.

```python
import mlflow.pyfunc
import joblib

class PDFModelWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = joblib.load("/path/to/xgboost_model.pkl")

    def predict(self, context, model_input):
        # Perform inference
        return self.model.predict(model_input)

# Log the model
client.mlflow.pyfunc.log_model(artifact_path="xgboost_model", python_model=PDFModelWrapper())
```

## Deploy with Kserve:
After logging the model, deploy it using Kserve.
Provide a REST endpoint for model inference.

```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "re"
  namespace: "modelhub"
  labels:
    azure.workload.identity/use: "true"
spec:
  predictor:
    model:
      modelFormat:
        name: mlflow
      protocolVersion: v2
      storageUri: "https://autonomizestorageaccount.blob.core.windows.net/mlflow/27/e5edc75c09d9470dadc42bd301ee8a8f/artifacts/reinfer_model"
      resources:
        limits:
          cpu: "3"
          memory: "16Gi"
          # nvidia.com/gpu: "1"
        requests:
          cpu: "3"
          memory: "16Gi"
    serviceAccountName: "genesis-platform-sa"
    tolerations:
      - key: "sku"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
```

## Examples
Here are additional examples to help you get started:

Logging Training and Evaluation Runs

```python
with client.start_run(run_name="Training Run"):
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    # Log parameters and metrics
    client.mlflow.log_param("model", "XGBoost")
    client.mlflow.log_metric("accuracy", accuracy)

    # Save and log the model
    joblib.dump(model, "xgboost_model.pkl")
    client.mlflow.log_artifact("xgboost_model.pkl")
```

## Managing Datasets
```python
from modelhub import load_dataset

# Load dataset
dataset = load_dataset("my_custom_dataset", version=2)

# Convert to pandas
df = pd.DataFrame(dataset["train"])

# Perform operations on the dataset
print(df.head())
```

## Using Blob Storage for Dataset
```python
# Set up blob storage config in YAML
blob_storage_config = "blob_storage_config.yaml"

# Load dataset from blob storage
dataset = load_dataset("my_dataset", blob_storage_config=blob_storage_config)
```
## Submitting a Pipeline
```python
from modelhub.clients import PipelineManager

# Submit and start the pipeline
pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))
pipeline = pipeline_manager.start_pipeline("pipeline.yaml")

print(f"Pipeline started with ID: {pipeline['id']}")
```

## Feedback & Contributions
Feel free to raise issues, submit PRs, or suggest features for the ModelHub SDK on our GitHub repository.

For feedback or support, please reach out to the ModelHub team directly.
