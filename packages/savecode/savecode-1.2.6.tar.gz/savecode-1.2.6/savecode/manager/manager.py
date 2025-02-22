"""
savecode/manager/manager.py - Manager for savecode plugins. Coordinates the pipeline of tasks.
Version: 1.2.1
"""

# Global registry for plugins
PLUGIN_REGISTRY = []

def register_plugin(cls):
    """
    Decorator to register a plugin class.
    The plugin must implement a public `run(context)` method.
    
    :param cls: The plugin class to register.
    :return: The original class.
    """
    PLUGIN_REGISTRY.append(cls())
    return cls

def run_plugins(context):
    """
    Run all registered plugins in sequence using the given context.
    
    :param context: Dictionary containing the context and shared data.
    """
    for plugin in PLUGIN_REGISTRY:
        plugin.run(context)

def list_plugins():
    """
    List the names of all registered plugins.
    
    :return: List of plugin class names.
    """
    return [plugin.__class__.__name__ for plugin in PLUGIN_REGISTRY]
