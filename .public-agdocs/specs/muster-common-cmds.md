add an opt to "agro muster": -c/--common-cmd used as e.g. "agro muster -c testq output/add.about.{1,2}" 

- When the -c flag is used with an argument, agro will look up the argument passed in the -c flag (e.g. "testq") the common command in the config file used passed into muster as the command_str.
- When running with -c no command_str is required. so make the command/command_str arg optional but only when the -c flag and associated argument are passed.
- Provide a useful error message to the user when the command is not found by explaining whether the config file and setting were found, and whether the command itself was found.
Add the logic for these steps to muster processing.

Also, add associated artifacts for muster-common-commands in config for it as well in MUSTER_COMMON_CMDS where there will be key/value pairs of:
- key: string (no spaces, only underscore of dash) 
- value: bash command
This will one default entry to start:
- key: testq 
- value: uv run pytest --tb=no -q

