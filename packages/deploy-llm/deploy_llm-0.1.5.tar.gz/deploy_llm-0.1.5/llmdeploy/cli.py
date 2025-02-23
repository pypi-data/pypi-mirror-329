import click
from llmdeploy.model_manager import deploy_model, list_models, list_deployed_models, remove_model, run_inference

@click.group()
def cli():
    """CLI tool to deploy and manage models from Ollama and Hugging Face."""
    pass

@click.command()
@click.option('--model', required=True, help="Model name to deploy")
@click.option('--source', default="ollama", type=click.Choice(["ollama", "huggingface"]), help="Source of the model (default: ollama)")
def deploy(model, source):
    """Deploy a model from Ollama or Hugging Face."""
    click.echo(deploy_model(model, source))

@click.command(name="list")
def list_cmd():
    """List all locally available models."""
    click.echo(list_models())

@click.command(name="list-deployed")
def list_deployed_cmd():
    """List deployed models tracked by this tool."""
    click.echo(list_deployed_models())

@click.command()
@click.option('--model', required=True, help="Model name to remove")
def remove(model):
    """Remove a deployed model."""
    click.echo(remove_model(model))

@click.command()
@click.option('--model', required=True, help="Model name to query")
@click.option('--prompt', required=True, help="Prompt to send to the model")
def query(model, prompt):
    """Run inference on a model."""
    click.echo(run_inference(model, prompt))

cli.add_command(deploy)
cli.add_command(list_cmd)
cli.add_command(list_deployed_cmd)
cli.add_command(remove)
cli.add_command(query)

if __name__ == "__main__":
    cli()
