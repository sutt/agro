allow the agent_type parameter to be infered in the absence of -a flag. We infer the agent_type from exec-cmd if passed absed on the criterion is a recognized agenttype in the name of the exec-cmd, e.g. "gemini" is in "mgemini.sh"

likewise infer the exec command if not passed from cli based off the agent type supplied in the -a flag if passed.