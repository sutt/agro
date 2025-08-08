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
    'AGENT_TYPE': 'aider',
    'AGENT_CONFIG': {
        'aider': {
            'task_file_arg_template': ['-f', '{task_file}'],
            'args': [
                "--yes",
                "--no-check-update",
                "--no-attribute-author",
                "--no-attribute-committer",
                "--no-attribute-co-authored-by",
            ]
        },
        'claude': {
            'task_file_arg_template': None,
            'args': [
                "-d",
                "--allowedTools",
                "Write Edit MultiEdit",
                "--max-turns",
                "30",
                "-p",
            ]
        },
        'gemini': {
            'task_file_arg_template': None,
            'args': [
                "-y",
            ],
        }
    },
    'AGENT_TIMEOUTS': {
        'aider': 0,  # 0 means no timeout is applied.
        'claude': 600,
        'gemini': 600,  # 10 minutes timeout for gemini calls
    },
    'MUSTER_DEFAULT_TIMEOUT': 20,
    'MUSTER_COMMON_CMDS': {
        'testq': {'cmd': 'uv run pytest --tb=no -q'},
        'server-start': {
            'cmd': 'uv run python app/main.py > server.log 2>&1 & echo $! > server.pid',
            'timeout': None,
        },
        'server-kill': {'cmd': 'kill $(cat server.pid) && rm -f server.pid server.log'},
    },
    'AGRO_EDITOR_CMD': 'code',
    'ENV_SETUP_CMDS': [
        'uv venv',
        'uv sync --quiet --all-extras',
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
                    if 'AGENT_TIMEOUTS' in user_config and isinstance(user_config['AGENT_TIMEOUTS'], dict):
                        config['AGENT_TIMEOUTS'].update(user_config.pop('AGENT_TIMEOUTS'))

                    if 'AGENT_CONFIG' in user_config and isinstance(user_config['AGENT_CONFIG'], dict):
                        user_agent_config = user_config.pop('AGENT_CONFIG')
                        for agent_name, agent_data in user_agent_config.items():
                            if agent_name in config['AGENT_CONFIG']:
                                config['AGENT_CONFIG'][agent_name].update(agent_data)
                            else:
                                config['AGENT_CONFIG'][agent_name] = agent_data

                    if 'MUSTER_COMMON_CMDS' in user_config and isinstance(user_config['MUSTER_COMMON_CMDS'], dict):
                        user_muster_cmds = user_config.pop('MUSTER_COMMON_CMDS')
                        for key, value in user_muster_cmds.items():
                            if (
                                key in config['MUSTER_COMMON_CMDS']
                                and isinstance(config['MUSTER_COMMON_CMDS'][key], dict)
                                and isinstance(value, dict)
                            ):
                                config['MUSTER_COMMON_CMDS'][key].update(value)
                            else:
                                config['MUSTER_COMMON_CMDS'][key] = value

                    config.update(user_config)
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse config file {config_path}. Using default values. Error: {e}", file=sys.stderr)

    valid_agent_types = {"aider", "gemini", "claude"}
    agent_type = config.get('AGENT_TYPE')
    if agent_type not in valid_agent_types:
        valid_types_str = ", ".join(sorted(list(valid_agent_types)))
        print(f"Error: Invalid AGENT_TYPE '{agent_type}'. Must be one of {valid_types_str}.", file=sys.stderr)
        sys.exit(1)

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
AGENT_TYPE = _config['AGENT_TYPE']
AGENT_CONFIG = _config['AGENT_CONFIG']
AGENT_TIMEOUTS = _config['AGENT_TIMEOUTS']
MUSTER_DEFAULT_TIMEOUT = _config['MUSTER_DEFAULT_TIMEOUT']
MUSTER_COMMON_CMDS = _config['MUSTER_COMMON_CMDS']
AGRO_EDITOR_CMD = _config['AGRO_EDITOR_CMD']
ENV_SETUP_CMDS = _config['ENV_SETUP_CMDS']

# App Env Replication for Configs
BASE_API_PORT = int(_config['BASE_API_PORT'])

