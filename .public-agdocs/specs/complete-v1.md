let's add cli completion via argcomplete.

start by adding cli completion for the subcommands. (later we'll add dynamic completions for arguments)

so when I type "agro <TAB>" it should present me with the available subcommands. Or if I type "agro dif<TAB>" it should complete to "agro diff"