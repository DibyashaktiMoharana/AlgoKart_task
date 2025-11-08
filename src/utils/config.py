"""Configuration utilities"""

import os
import sys


def get_port():
    """Get server port from CLI args > ENV > default (4000)"""
    # Check --port argument
    for i, arg in enumerate(sys.argv[:-1]):
        if arg == '--port':
            try:
                return int(sys.argv[i + 1])
            except (ValueError, IndexError):
                pass
    
    # Check PORT environment variable
    if port := os.environ.get('PORT'):
        try:
            return int(port)
        except ValueError:
            pass
    
    return 4000
