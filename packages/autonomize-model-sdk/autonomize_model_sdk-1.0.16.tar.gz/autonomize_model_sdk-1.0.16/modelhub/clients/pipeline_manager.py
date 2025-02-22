""" This module contains the PipelineManager class for creating and managing pipelines. """

import requests
import yaml

from ..core import BaseClient, ModelHubException
from ..models import PipelineCreateRequest, SubmitPipelineRequest
from ..utils import encode_file


class PipelineManager(BaseClient):
    """Manager for creating and managing pipelines."""

    def __init__(self, base_url=None, client_id=None, client_secret=None, token=None):
        """
        Initializes a new instance of the PipelineManager class.

        Args:
            base_url (str): The base URL of the pipeline manager.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.
        """
        super().__init__(base_url, client_id, client_secret, token)

    def load_config(self, config_path, pyproject_path=None):
        """
        Loads the pipeline configuration from a YAML file.
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if pyproject_path is not None:
            config["pyproject"] = encode_file(pyproject_path)

        # Ensure stages have proper defaults
        for stage in config["stages"]:
            # Ensure depends_on is a list
            if "depends_on" not in stage:
                stage["depends_on"] = []
            elif stage["depends_on"] is None:
                stage["depends_on"] = []

            # Handle script encoding
            if "script" in stage and stage["script"]:
                stage["script"] = encode_file(stage["script"])

            # Handle requirements encoding
            if "requirements" in stage and stage["requirements"]:
                stage["requirements"] = encode_file(stage["requirements"])

            # Ensure other fields have proper defaults
            stage["params"] = stage.get("params", {})
            stage["tolerations"] = stage.get("tolerations", [])
            stage["node_selector"] = stage.get("node_selector", {})

            # Handle blob_storage_config
            if "blob_storage_config" in stage and stage["blob_storage_config"]:
                blob_storage_config = stage["blob_storage_config"]
                if not all(
                    key in blob_storage_config
                    for key in ["container", "blob_url", "mount_path"]
                ):
                    raise ModelHubException(
                        f"Invalid blob_storage_config for stage {stage['name']}. "
                        "It must include 'container', 'blob_url', and 'mount_path'."
                    )

        pipeline_request = PipelineCreateRequest(**config)
        return pipeline_request

    def start_pipeline(self, config_path, pyproject_path=None):
        """
        Starts a pipeline based on the configuration file.

        Args:
            config_path (str): The path to the YAML configuration file.
            pyproject_path (str, optional): The path to the pyproject. Defaults to None.

        Returns:
            dict: The response from the API.
        """
        pipeline = self.create_or_update(config_path, pyproject_path)
        return self.submit(pipeline["pipeline_id"])

    def create_or_update(self, config_path, pyproject_path=None):
        """
        Creates or updates a pipeline based on the configuration file.

        Args:
            config_path (str): The path to the YAML configuration file.
            pyproject_path (str, optional): The path to the pyproject. Defaults to None.

        Returns:
            dict: The response from the API.
        """
        pipeline_request = self.load_config(config_path, pyproject_path)
        existing_pipeline = self.search_pipeline(pipeline_request.name)
        if existing_pipeline:
            return self.put(
                f"pipelines/{existing_pipeline['pipeline_id']}",
                json=pipeline_request.dict(),
            )
        else:
            return self.post("pipelines", json=pipeline_request.dict())

    def search_pipeline(self, name):
        """
        Searches for a pipeline by name.

        Args:
            name (str): The name of the pipeline to search for.

        Returns:
            dict: The existing pipeline if found, None otherwise.
        """
        try:
            existing_pipeline = self.get(f"pipelines/search?name={name}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                existing_pipeline = None
            else:
                raise ModelHubException("Failed to search for pipeline.") from e
        return existing_pipeline

    def submit(self, pipeline_id):
        """
        Submits a pipeline for execution.

        Args:
            pipeline_id (str): The ID of the pipeline to submit.

        Returns:
            dict: The response from the API.
        """
        submit_request = SubmitPipelineRequest(
            modelhub_base_url=self.base_url,
            modelhub_client_id=self.client_id,
            modelhub_client_secret=self.client_secret,
        )
        return self.post(f"pipelines/{pipeline_id}/submit", json=submit_request.dict())
