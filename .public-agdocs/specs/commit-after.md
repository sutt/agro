when the agent_Type aider runs, it finishes by leaving a git commit on the worktrees branch. but when gemini and calude run they don't do a commit even afte editing files.

i want to add a feature to exec that will create the commit for gemini and claude runs that checks if the agent has finished running and if so creates a git commit of all changes

Add this feature as default behavior and add a command line arg to turn this off.