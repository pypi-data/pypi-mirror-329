"""
savecode/plugins/extra_args.py - Plugin to process and parse extra command-line arguments into key-value pairs.
"""

import logging
from typing import Any, Dict, List
from savecode.plugin_manager.manager import register_plugin

logger = logging.getLogger(__name__)

def parse_extra_args(extra_args: List[str]) -> Dict[str, Any]:
    """
    Parses a list of extra command-line arguments into a dictionary.

    - Arguments containing '=' are split into key and value.
    - Arguments without '=' are treated as boolean flags (value True).

    :param extra_args: List of extra argument strings.
    :return: Dictionary of parsed arguments with keys as strings and values as either string or bool.
    """
    parsed: Dict[str, Any] = {}
    for arg in extra_args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            parsed[key] = value
        else:
            parsed[arg] = True
    return parsed

@register_plugin
class ExtraArgsPlugin:
    """
    Plugin that processes extra command-line arguments by parsing them into a structured key-value dictionary.
    
    Responsibilities:
      - Logs any extra arguments provided.
      - Parses arguments in the form key=value into a dictionary.
      - Treats standalone arguments as boolean flags (True).
      - Stores the parsed arguments in the shared context under the key 'parsed_extra_args'.
    """
    def run(self, context: Dict[str, Any]) -> None:
        extra_args: List[str] = context.get('extra_args', [])
        if extra_args:
            logger.info("Extra arguments provided: %s", extra_args)
            parsed: Dict[str, Any] = parse_extra_args(extra_args)
            context['parsed_extra_args'] = parsed
            logger.info("Parsed extra arguments: %s", parsed)