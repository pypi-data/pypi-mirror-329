import os
from typing import Dict, Any


def exists(path: str) -> bool:
    """Check if path exists"""
    return os.path.exists(path)


def is_directory(path: str) -> bool:
    """Check if path is a directory"""
    return os.path.isdir(path)


def get_read_file(path: str) -> Dict[str, Any]:
    """Get file info and stream for reading"""
    stats = os.stat(path)
    return {
        'name': os.path.basename(path),
        'stream': open(path, 'rb'),
        'stats': stats
    }
