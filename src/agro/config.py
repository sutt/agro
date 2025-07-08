import sys
import yaml
from pathlib import Path

# Default configuration values
DEFAULTS = {
    'AGDOCS_DIR': '.agdocs',
    'PUBLIC_AGDOCS_DIR': '.public-agdocs',
    'WORKTREE_DIR': './trees',
    'WORKTREE_BRANCH_PREFIX': 'tree/t',
    'WORKTREE_OUTPUT_BRANCH_PREFIX': 'output/',
    'EXEC_CMD_DEFAULT': 'aider',
    'BASE_API_PORT': 8000,
    'DB_BASE_PORT': 5432,
    'DB_CONTAINER_NAME_PREFIX': 'tf-db',
    'API_CONTAINER_NAME_PREFIX': 'tf-api',
    'DB_VOLUME_NAME_PREFIX': 'tf-db-data',
}

def _load_config():
    """Loads configuration from YAML file, falling back to defaults."""
    # The config file path is fixed relative to the project root.
    config_path = Path(DEFAULTS['AGDOCS_DIR']) / 'conf' / 'agro.conf.yml'
    
    config = DEFAULTS.copy()

    if config_path.is_file():
        with open(config_path, 'r') as f:
            try:
                user_config = yaml.safe_load(f)
                if user_config:
                    config.update(user_config)
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse config file {config_path}. Using default values. Error: {e}", file=sys.stderr)

    return config

_config = _load_config()

# Agro-Specific Configs
WORKTREE_DIR = _config['WORKTREE_DIR']
AGDOCS_DIR = _config['AGDOCS_DIR']
PUBLIC_AGDOCS_DIR = _config['PUBLIC_AGDOCS_DIR']
WORKTREE_BRANCH_PREFIX = _config['WORKTREE_BRANCH_PREFIX']
WORKTREE_OUTPUT_BRANCH_PREFIX = _config['WORKTREE_OUTPUT_BRANCH_PREFIX']

# Agro-Agent Configs
EXEC_CMD_DEFAULT = _config['EXEC_CMD_DEFAULT']

# App Env Replication for Configs
BASE_API_PORT = int(_config['BASE_API_PORT'])
DB_BASE_PORT = int(_config['DB_BASE_PORT'])
DB_CONTAINER_NAME_PREFIX = _config['DB_CONTAINER_NAME_PREFIX']
API_CONTAINER_NAME_PREFIX = _config['API_CONTAINER_NAME_PREFIX']
DB_VOLUME_NAME_PREFIX = _config['DB_VOLUME_NAME_PREFIX']
