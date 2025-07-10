currently we run which works for this project but fails  for other simple 
'uv sync --quiet --group test' which works for this project but fails on other projects.

Let's find a solution  that works on this repo (sync the worktree env with all packages listed and the test packages (not dev)) and also works with other common simple (remeber they can still configure it themselves but it should work out of the box for default)

Change either the pyporject.toml or the uv sync setting in env setup 