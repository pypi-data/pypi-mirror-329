import os
import json
from pathlib import Path
from typing import TypeVar, Dict, Optional, Any

ZETIC_ENV_FILE_NAME = ".zeticrc"
INDENTATION = 2

# Type definitions
T = TypeVar('T')
ZeticConfig = Dict[str, Any]


def get_config(env_file_path: str) -> ZeticConfig:
    """Load configuration from file, create if doesn't exist"""
    try:
        with open(env_file_path, 'r') as f:
            return json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(env_file_path), exist_ok=True)
        # Create empty config file
        with open(env_file_path, 'w') as f:
            f.write(json.dumps({}, indent=INDENTATION))
        return {}


def save_config(env_file_path: str, config: ZeticConfig) -> None:
    """Save configuration to file, removing None values"""
    filtered_config = {
        key: value for key, value in config.items()
        if value is not None
    }

    with open(env_file_path, 'w') as f:
        f.write(json.dumps(filtered_config, indent=INDENTATION))


def get(key: str) -> Optional[Any]:
    """Get a value from config by key"""
    env_file_path = os.path.join(os.path.expanduser('~'), ZETIC_ENV_FILE_NAME)
    config = get_config(env_file_path)
    return config.get(key)


def set(key: str, data: Any) -> None:
    """Set a value in config by key"""
    env_file_path = os.path.join(os.path.expanduser('~'), ZETIC_ENV_FILE_NAME)
    config = get_config(env_file_path)
    config[key] = data
    save_config(env_file_path, config)


def remove(key: str) -> None:
    """Remove a value from config by key"""
    set(key, None)
