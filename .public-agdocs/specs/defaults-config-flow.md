refactor the config file init generation logic for the following request:

in core._get_config_template() utilize values supplied from config.DEFAULTS everywhere possible. The idea is to make DEFAULTS the upstream source of truth from writing out the config file with the defaults.

For example the config template already imports the default value here:
# AGDOCS_DIR: {config.DEFAULTS['AGDOCS_DIR']}

But the config template doesnt use the default (and it is available):
# ENV_SETUP_CMDS:
#   - 'uv venv'
#   - 'uv sync --quiet --all-extras'

Add all logic for adding lists and dictionaries into the template where appropriate.
