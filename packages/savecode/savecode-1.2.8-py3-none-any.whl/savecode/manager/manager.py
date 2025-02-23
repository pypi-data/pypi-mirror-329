"""
savecode/manager/manager.py - Manager for savecode plugins. Coordinates the pipeline of tasks.
This module now registers plugin classes and delays their instantiation until runtime,
facilitating future enhancements such as dependency injection or configuration.
"""

from typing import Any, Dict, List, Type

# Global registry for plugin classes
PLUGIN_REGISTRY: List[Type] = []

def register_plugin(cls: Type) -> Type:
    """
    Decorator to register a plugin class.
    The plugin must implement a public `run(context)` method.

    By storing the class instead of an instance, instantiation is delayed until run-time.
    
    :param cls: The plugin class to register.
    :return: The original class.
    """
    PLUGIN_REGISTRY.append(cls)
    return cls

def run_plugins(context: Dict[str, Any]) -> None:
    """
    Instantiate and run all registered plugins in sequence using the given context.
    
    This delayed instantiation approach allows for future enhancements such as passing configuration
    or dependencies to the plugin constructors.
    
    :param context: Dictionary containing the context and shared data.
    """
    for plugin_class in PLUGIN_REGISTRY:
        plugin_instance = plugin_class()  # Delayed instantiation
        plugin_instance.run(context)

def list_plugins() -> List[str]:
    """
    List the names of all registered plugin classes.
    
    :return: List of plugin class names.
    """
    return [cls.__name__ for cls in PLUGIN_REGISTRY]