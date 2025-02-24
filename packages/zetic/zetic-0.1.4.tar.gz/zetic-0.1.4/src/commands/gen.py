import os
import click
from typing import List
import asyncio
from ..client import client
from ..utils.filesystem import exists, is_directory, get_read_file


async def upload_model(model_path: str, project_path: str, input_paths: List[str]):
    """Upload model and input files to server"""
    click.echo("Starting upload process...")
    click.echo(f"Project: {project_path}")
    click.echo(f"Model Path: {model_path}")

    try:
        # Prepare multipart form data
        files = []

        # Add model file
        model_file = get_read_file(model_path)
        files.append(
            ('file', (model_file['name'], model_file['stream'], 'application/octet-stream'))
        )

        # Add input files
        for input_path in input_paths:
            input_file = get_read_file(input_path)
            files.append(
                ('inputs', (input_file['name'], input_file['stream'], 'application/octet-stream'))
            )

        # Make request
        response = client.post(
            f"/p/{project_path}/models",
            files=files,
            timeout=None  # No timeout for large uploads
        )

        click.echo("Upload completed successfully!")
        click.echo("Model is converting...")
        click.echo(f"Your model key is {response.json()['tag']}")

    except Exception as e:
        if hasattr(e, 'response'):
            # Server responded with error
            click.echo(click.style(
                f"Upload failed with status: {e.response.status_code}", fg='red'))
            click.echo(click.style(
                f"Server response: {e.response.json()}", fg='red'))
        elif hasattr(e, 'request'):
            # No response received
            click.echo(click.style("No response received from server", fg='red'))
        else:
            click.echo(click.style(f"Upload failed: {str(e)}", fg='red'))
        raise click.Abort()


@click.command()
@click.option('-d', '--debug', is_flag=True, help='Output extra debugging')
@click.option('-p', '--project', required=True, help='Project name ex) zetic-ai/new-project')
@click.option('-i', '--input', 'input_paths', multiple=True, required=True,
              help='Input data ex) -i sample1.npy -i sample2.npy')
@click.argument('model_path', required=True)
def gen(debug: bool, project: str, input_paths: List[str], model_path: str):
    """Generate model from path"""
    # Debug logging
    if debug:
        click.echo("Debug mode enabled")
        click.echo(f"Options: project={project}, input_paths={input_paths}")
        click.echo(f"Model path: {model_path}")

    try:
        # Resolve model path
        model_absolute_path = os.path.abspath(model_path)

        # Validate model path
        if not exists(model_absolute_path):
            raise click.BadParameter(
                f"Model path does not exist: {model_absolute_path}")

        if is_directory(model_absolute_path):
            raise click.BadParameter(
                f"Model path must be a file: {model_absolute_path}")

        # Validate and collect input paths
        collected_input_paths = []
        for input_path in input_paths:
            input_absolute_path = os.path.abspath(input_path)

            if not exists(input_absolute_path):
                raise click.BadParameter(
                    f"Input path does not exist: {input_absolute_path}")

            if is_directory(input_absolute_path):
                raise click.BadParameter(
                    f"Input path must be a file: {input_absolute_path}")

            collected_input_paths.append(input_absolute_path)

        click.echo(
            f"Uploading model from {model_absolute_path} to project {project}")

        # Run upload in async context
        asyncio.run(upload_model(
            model_absolute_path,
            project,
            collected_input_paths
        ))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'))
        raise click.Abort()
