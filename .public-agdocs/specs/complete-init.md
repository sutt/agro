Add another step to "agro init" that will add cli completion setup to the bash shell.

Also add "--completions [perm]" flag to the init command to specifically carry out just this step.

There are two ways in which cli completions can be added to the shell:
- current shell
- peremanent via bashrc

In the default case, either "agro init" or "agro init --completion" initiate the "current shell" process. When "agro init --completions perm" is called do the "permanent via bashrc" process.

Completions use argcomplete and uv / uvx.

For the current shell sessions you use the argcomplete.shellcode method. Or if ne should invoke this shell command and get it to apply to the current shell:
> eval "$(register-python-argcomplete agro)"


For the permanent process write this to the .bashrc file:
> # agro cli completions
> eval "$(uvx --from argcomplete register-python-argcomplete agro)"

Before running the completion enabling commands, perform these checks, and if not met provide an informative err message along with a pointer to visit the docs to learn more.
- check that the shell is bash
- check that uv / uvx is installed (for perm)