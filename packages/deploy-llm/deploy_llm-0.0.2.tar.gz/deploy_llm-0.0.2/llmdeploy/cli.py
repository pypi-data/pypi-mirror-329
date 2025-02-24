import click
from llmdeploy.model_manager import deploy_model, list_models, remove_model, run_inference

@click.group()
def cli():
    """LLMDeploy CLI - Manage and deploy LLM models."""
    pass

@click.command()
@click.argument("model_name")
@click.option("--model_type", required=True, type=click.Choice(["text", "multimodal"]), help="Model type (text/multimodal).")
def deploy(model_name, model_type):
    """Deploy a model from Ollama."""
    result = deploy_model(model_name, model_type)
    click.echo(result)

@click.command()
def list():
    """List deployed models."""
    models = list_models()
    click.echo(models)

@click.command()
@click.argument("model_name")
def remove(model_name):
    """Remove a deployed model."""
    result = remove_model(model_name)
    click.echo(result)

@click.command()
@click.argument("model_name")
@click.option("--input", help="Text input for inference.")
@click.option("--image-path", help="Path to an image (for multimodal models).")
def infer(model_name, input, image_path):
    """Run inference on a deployed model."""
    result = run_inference(model_name, input_text=input, image_path=image_path)
    click.echo(result)

cli.add_command(deploy)
cli.add_command(list)
cli.add_command(remove)
cli.add_command(infer)

if __name__ == "__main__":
    cli()
