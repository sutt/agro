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
    'AGRO_EDITOR_CMD': 'code',
    'ENV_SETUP_CMDS': [
        'uv venv',
        'uv sync --quiet --group test',
    ],
    'BASE_API_PORT': 8000,
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
AGRO_EDITOR_CMD = _config['AGRO_EDITOR_CMD']
ENV_SETUP_CMDS = _config['ENV_SETUP_CMDS']

# App Env Replication for Configs
BASE_API_PORT = int(_config['BASE_API_PORT'])

