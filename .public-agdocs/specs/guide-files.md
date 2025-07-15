we're adding functionality for guide files:
- by default these are .agdocs/guides/.md files 
- these files provide guides and conventions for the coding agents dispatched
- there will be one main one GUIDE.md and there can be others added by the user. Ideally we don't want to have to hard code these other files

tasks:
- when running agro init, create a "guides" directory in .agdocs and a GUIDE.md in it
- when running exec copy the .md contents of guides directory to the agent's worktree in .agswap/guides/
- when dispatching an agent give it read-access to the guide file(s).
    - for claude: prepend "@.agswap/guides/* " at the beginning of the task text (what is read in from the task file). 
    - for aider: add [multiple] --read <fn> flags where <fn> is the path to each of the guide files copied.
