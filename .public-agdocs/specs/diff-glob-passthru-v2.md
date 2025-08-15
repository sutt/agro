enable agro diff [diff_args] to pass through a path like "agro diff -- my/path that runs "git diff -- my/path"

From the git documentation on git diff:
git diff [<options>] [<commit>] [--] [<path>...]

This has been attempted to be committed but currently:

This one works:
$ agro diff output --stat -- tests
gives:
--- Diff for t1 (output/add-about.1) ---
opts: ['--stat', '--', 'tests']
branch_patterns: ['output']
original: ['git', 'diff', '--stat', 'tree/t1', 'HEAD', '--', 'tests']
$ git diff --stat tree/t1 HEAD -- tests

This one doesn't work:
$ agro diff output  -- tests
gives:
--- Diff for t1 (output/add-about.1) ---
opts: []
branch_patterns: ['output', 'tests']
original: ['git', 'diff', 'tree/t1', 'HEAD']
$ git diff tree/t1 HEAD

Make it work for both.