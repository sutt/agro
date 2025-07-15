when launching a gemini agent from exec:

- check if a .gemini directory exists in at the root of the git worktree when you go to launch:
    - if yes:  throw a warning explaining agent will not have access to guide files, and don't proceed with the next steps
    - if no: proceed with the following:

- create a .gemini directory at the project root (within the agent's workingtree) 
- add a .gitignore file to .gemini with contents "*" in order for this to not get tracker
- add a settings.json in .gemini with contents:
{
    "contextFileName": [
        "<fn1>",
        "<fn2>",
        ...
    ]
}
    - where fn1, fn2, ... are the relative paths to the files copied into .agswap/guides/ for that worktree (not this is done in both aider and claude agents as well, but has different cli structure).