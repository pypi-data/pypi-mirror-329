import click


@click.group()
def cli():
    """OneSource CLI tool."""
    pass


@cli.command()
@click.option("-m", "--message", required=True, help="Message to process")
def run(message):
    """Run the OneSource process with a given message."""
    click.echo(f"Processing message: {message}")
    # Add your actual processing logic here


@cli.command()
@click.option("-c", "--config", default="config.json", help="Path to config file")
def init(config):
    """Initialize OneSource with a config file."""
    click.echo(f"Initializing with config: {config}")
    # Add initialization logic here


if __name__ == "__main__":
    cli()
