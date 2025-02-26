# modelhub/cli.py
import argparse
import os

from modelhub.clients import (  # This uses your existing PipelineManager class
    PipelineManager,
)


def main():
    """
    PipelineManager CLI entrypoint.
    """
    parser = argparse.ArgumentParser(
        description="ModelHub Pipeline CLI - Manage and execute pipelines"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create the "start" subcommand
    start_parser = subparsers.add_parser("start", help="Start pipeline execution")
    start_parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="pipeline.yaml",
        help="Path to the pipeline YAML file (default: pipeline.yaml)",
    )
    start_parser.add_argument(
        "--mode",
        choices=["local", "cicd"],
        default="local",
        help="Execution mode: 'local' to run with local scripts \
        (and install dependencies using Poetry) \
        or 'cicd' for CI/CD mode",
    )
    # Only relevant in local mode: path to the pyproject.toml file.
    start_parser.add_argument(
        "--pyproject",
        type=str,
        default="pyproject.toml",
        help="Path to the pyproject.toml file (required for local mode)",
    )

    args = parser.parse_args()

    # Ensure the required environment variable is set.
    base_url = os.getenv("MODELHUB_BASE_URL")
    if not base_url:
        raise ValueError("MODELHUB_BASE_URL environment variable is not set.")

    # Initialize the PipelineManager.
    pipeline_manager = PipelineManager(base_url=base_url)

    if args.command == "start":
        pipeline_yaml = args.file
        mode = args.mode

        if mode == "local":
            pyproject_path = args.pyproject
            if not os.path.exists(pyproject_path):
                raise ValueError(f"pyproject.toml file not found at {pyproject_path}")
            print(
                f"Starting pipeline locally using {pipeline_yaml} with pyproject file {pyproject_path} ..."
            )
            # Pass both the YAML file and the pyproject.toml path.
            pipeline = pipeline_manager.start_pipeline(pipeline_yaml, pyproject_path)
            print("Pipeline started:", pipeline)
        elif mode == "cicd":
            print(f"Starting pipeline in CI/CD mode using {pipeline_yaml} ...")
            # In CI/CD mode, the Docker image already contains the required files.
            pipeline = pipeline_manager.start_pipeline(pipeline_yaml)
            print("Pipeline started in CI/CD mode:", pipeline)


if __name__ == "__main__":
    main()
