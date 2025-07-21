Make the following args optional in agro muster:
agro muster [command] [branch-pattern]

Add an opt to "agro muster": -c/--common-cmd which accepts a str argument.

CLI Conditions:
- command arg is optional only if -c is supplied.
    - so if no -c and no command supplied, the command is invalid.
    - so if -c is supplied with an argument, then the next arg passed will be the branch-pattern
- command and branch-pattern can be expected to provided positionally: the command string will always be before the branch
- when branch-pattern is empty the default should be to use WORKTREE_OUTPUT_BRANCH_PREFIX pattern.

CLI examples:
$ agro muster -c pytestq output/feat.
# command_cmd="pytestq" branch_pattern="output/feat"
$ agro muster 'uv run pytest'
# command="uv run pytest" 
$ agro muster -c pytestq "uv run pytest" output/
# invalid: command supplied with -c

Add the logic to convert the common_cmd into a bash command that will be run by muster across the worktrees:
- When the -c flag is used with an argument, agro will look up the argument passed in the -c flag (e.g. "testq") for the command supplied in the agro config file under MUSTER_COMMON_CMDS that has key/value pairs of:
    - key: string (no spaces, only underscore of dash) 
    - value: bash command
- Provide a useful error message to the user when the command is not found by explaining whether the config file and setting were found, and whether the command itself was found.
Add the logic for these steps to muster processing.

Also, add associated artifacts for muster-common-commands in config for it as well in MUSTER_COMMON_CMDS where there will be key/value pairs of:
- key: string (no spaces, only underscore of dash) 
- value: bash command
This will one default entry to start:
- key: testq 
- value: uv run pytest --tb=no -q

Add tests to validate this behavior and any other edge cases you can think of.