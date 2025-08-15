add a default timeout of 20 seconds to all commands run by muster, that will pass this through to subprocess.run.

Config and Args:
- add config and command lines options that can override the default value
- create a config var for this timeout amount in agro.conf.yml: MUSTER_DEFAULT_TIMEOUT which takes an integer value in seconds. Setting to null or 0 
- modify MUSTER_COMMON_CMDS to refactor the command string in a "cmd" key, and have an optional param "timeout" which overrides the MUSTER_DEFAULT_TIMEOUT value with the same convention of null or 0 maening no timeout. 
    - For "sever-start" command add a "timeout: null" entry as the default config + what will be written into the default agro.conf.yml 
- create a cli flag for agro muster "--timeout" that overrides the config and default values, that will use seconds and input value and use the value 0 to have no timeout.

Tests:
- Refactor any failing tests due to the change.
- Add tests for overriding default timeout functionality