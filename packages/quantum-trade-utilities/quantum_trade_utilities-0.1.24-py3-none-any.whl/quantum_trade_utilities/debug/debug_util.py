"""
Debugging utilities for Gilfoyle.
"""

import debugpy

def start_debug_server():
    """
    Start the debug server and wait for client connection.
    """
    debugpy.listen(5678)
    debugpy.wait_for_client()

def bp():
    """
    Breakpoint function for Gilfoyle.
    """
    return debugpy.breakpoint()