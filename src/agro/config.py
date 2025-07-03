import os
from dotenv import load_dotenv

# Load .env file if it exists to override defaults
load_dotenv()

# Default configuration, can be overridden in .env
WORKTREE_DIR = os.getenv('WORKTREE_DIR', './trees')
WORKTREE_BRANCH_PREFIX = os.getenv('WORKTREE_BRANCH_PREFIX', 'tree/t')
WORKTREE_OUTPUT_BRANCH_PREFIX = os.getenv('WORKTREE_OUTPUT_BRANCH_PREFIX', 'output/')
BASE_API_PORT = int(os.getenv('BASE_API_PORT', 8000))
DB_BASE_PORT = int(os.getenv('DB_BASE_PORT', 5432))
DB_CONTAINER_NAME_PREFIX = os.getenv('DB_CONTAINER_NAME_PREFIX', 'tf-db')
API_CONTAINER_NAME_PREFIX = os.getenv('API_CONTAINER_NAME_PREFIX', 'tf-api')
DB_VOLUME_NAME_PREFIX = os.getenv('DB_VOLUME_NAME_PREFIX', 'tf-db-data')
