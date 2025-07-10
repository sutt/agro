when the agent_type aider runs, it finishes by leaving a git commit on the worktrees branch. but when gemini and claude run they don't do a commit even afte editing files.

i want to add a feature to exec that will create the commit for gemini and claude runs that checks if the agent has finished running and if so creates a git commit of all changes made.

Add this feature as default behavior and add a command line arg to turn this off.

The feature should be non-blocking for agro / agro exec, such that the agro process exits and returns a prompt to the user after all the agents have been launched. 
But the feature must also be able to run in the background
Provide some debugging i can use to see if it's working and how it's working that will be available when agro is run with -vv