import pluggy

# Define the hook specification namespace
hookspec = pluggy.HookspecMarker("tilly")
hookimpl = pluggy.HookimplMarker("tilly")

# Plugin manager setup
plugin_manager = pluggy.PluginManager("tilly")

# Hook specification for registering commands
@hookspec
def til_command(cli):
    """Hook for adding commands to the tilly CLI."""
    pass

# Register default and external plugins
plugin_manager.load_setuptools_entrypoints("tilly")
