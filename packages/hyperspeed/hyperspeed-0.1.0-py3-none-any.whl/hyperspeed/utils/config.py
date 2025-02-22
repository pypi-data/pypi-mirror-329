import yaml
from pathlib import Path

DEFAULT_CONFIG = {
    'host': '0.0.0.0',
    'port': 8080,
    'max_connections': 100,
    'cache_ttl': 300
}

def load_config(file_path):
    try:
        with open(file_path) as f:
            return {**DEFAULT_CONFIG, **yaml.safe_load(f)}
    except FileNotFoundError:
        return DEFAULT_CONFIG