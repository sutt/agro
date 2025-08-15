refactor the cli passing to allow "agro diff" to accept diff_opts arguments when no branch-pattern supplied.

Currently this works:
> agro diff output --stat

But this does not:
> agro diff --stat

Allow this command to work.