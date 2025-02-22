from .cli import cli
from .plugin import plugin_manager

# Import built-in plugins or commands
import tilly.commands.hello

# Register built-in plugins
plugin_manager.register(tilly.commands.hello, "hello")

# Load plugins dynamically
plugin_manager.hook.til_command(cli=cli)

if __name__ == "__main__":
    cli()