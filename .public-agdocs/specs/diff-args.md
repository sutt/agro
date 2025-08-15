Change the form of the "agro diff" command:

before:
> agro diff [--stat] [branch-patterns]
after:
> agro diff [branch-patterns] [diff-opts]

- Remove the --stat option
- Add optional "diff-opts" after branch-patterns, which can be multiple options. 
    - the most common option will be "--stat"
- Note: for parsing the two optional that branch patterns will be an argument, and all opts will have one or two hyphens preceeding 

All "diff-opts" are passed through to the git diff command in options. Here's some documentation on the git diff command:
> git diff [<options>] [<commit>] [--] [<path>...]
common diff options:
  -z            output diff-raw with lines terminated with NUL.
  -p            output patch format.
  -u            synonym for -p.
  --stat        show diffstat instead of patch.
...