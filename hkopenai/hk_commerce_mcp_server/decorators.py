"""
Module for creating tool registry decorators.

This module provides a function to create a decorator that can register
tools and allow lookup by name for use in the MCP server.
"""

def create_tool_registry():
    """Create a tool registry decorator that tracks decorated functions by name.

    Returns:
        A decorator function that can be used to register tools and provides
        a get(name) method to lookup registered tools by function name.
    """
    registry = {}

    def tool_decorator(description=None):
        def decorator(f):
            registry[f.__name__] = f
            return f

        return decorator

    # Add lookup capability to the decorator
    tool_decorator.get = registry.get
    return tool_decorator
