allow all agent_types to be configured to have a timeout preprended to their launch command
have claude be configured for a 600 s timeout default as well (leave aider without timeout).
Have this setting explicitly call out that 0 settings overrides the default timeout if any (thus aider is 0)
have claude be configured to have the following additional flags
 --max-tries 30
write all the default flags to each agent into the config when initialized. (but these will start commented out so make sure that in the absence of finding them specified in the user config, you run the default flags anyways)