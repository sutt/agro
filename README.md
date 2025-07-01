# agscript

A script to manage git worktrees for agent-based development. This tool simplifies creating, managing, and running processes within isolated worktrees, each with its own environment configuration.

## Configuration

`agscript` is configured via environment variables, which can be placed in a `.env` file in the root of your project. A `.env.example` file can be used as a template.

The following variables can be configured:

- `WORKTREE_DIR`: The directory to store worktrees. (Default: `./trees`)
- `WORKTREE_BRANCH_PREFIX`: The prefix for worktree-specific branches. (Default: `tree/t`)
- `WORKTREE_OUTPUT_BRANCH_PREFIX`: The prefix for branches created by the `exec` command. (Default: `output/`)
- `BASE_API_PORT`: The base port for the API service in each worktree. The worktree index is added to this. (Default: `8000`)
- `DB_BASE_PORT`: The base port for the database service. (Default: `5432`)
- `DB_CONTAINER_NAME_PREFIX`: Prefix for the Docker container name for the database. (Default: `tf-db`)
- `API_CONTAINER_NAME_PREFIX`: Prefix for the Docker container name for the API. (Default: `tf-api`)
- `DB_VOLUME_NAME_PREFIX`: Prefix for the Docker volume name for the database. (Default: `tf-db-data`)

## Installation

You can install this tool and its dependencies from the local project directory using `uv`. Make sure you have `uv` installed.

From the root of the project directory, run:
