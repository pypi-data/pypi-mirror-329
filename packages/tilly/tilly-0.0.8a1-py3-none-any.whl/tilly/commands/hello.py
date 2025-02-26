from click import echo
from ..plugin import hookimpl

# Define a hook implementation for the TIL CLI
@hookimpl
def til_command(cli):
    """Add a sample TIL command."""

    # Define the 'hello' command within the CLI
    @cli.command()
    def hello():
        """Say hello."""
        echo("Hello from the TIL CLI!")