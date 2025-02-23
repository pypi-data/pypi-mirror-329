"""
savecode/plugin_manager/manager.py - Manager for savecode plugins with enhanced error isolation.
This module registers plugin classes and delays their instantiation until runtime,
facilitating future enhancements such as dependency injection or configuration.
"""

from typing import Any, Dict, List, Type
import logging

logger = logging.getLogger(__name__)

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
    Each plugin is executed in isolation; errors in one plugin are logged without halting the pipeline.
    
    :param context: Dictionary containing the context and shared data.
    """
    for plugin_class in PLUGIN_REGISTRY:
        plugin_instance = plugin_class()  # Delayed instantiation
        try:
            plugin_instance.run(context)
        except Exception as e:
            logger.error("Error running plugin %s: %s", plugin_class.__name__, e, exc_info=True)

def list_plugins() -> List[str]:
    """
    List the names of all registered plugin classes.
    
    :return: List of plugin class names.
    """
    return [cls.__name__ for cls in PLUGIN_REGISTRY]