add a command "surrender" to agscript that will kill running processes of aider/maider.

Note the pid's are stored in .agdocs/swap/t<N>.pid where N is the index.

This command will take an argument similiar to <indices> for muster for which worktrees instances being run there on the index numbers. If no argument is supplied here, assume "all".

This command should first do a dry run to figure out which pid's it has available to it and which can be found to be running (e.g grepped in ps aux) and print this to command line.

The command should prompt the user Y/n to continue with the kill process, perform the process if confirmed, and report the results. 