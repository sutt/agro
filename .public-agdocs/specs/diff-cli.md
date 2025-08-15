Refactor the "agro diff" cli:

Enable agro diff [diff-opts] to pass through a path like "agro diff -- my/path that runs "git diff -- my/path"

Note for agro diff cli the cli hint says, showing both branch-patterns 
 diff [branch-patterns] [diff-opts]

From the git documentation on git diff we're looking to do this pattern
git diff [<options>] [<commit>] [--] [<path>...]

This means if you find a path argument in the diff-opts of the form "-- <some-path>" even within a larger string of args "... -- <some-path> ..." then the path stuff should go at the end of the git diff command string, but other args passed to the git diff (.e.g. --stat) should go in the git diff options place.

Here's some test cases and how they should work:

$ agro diff --stat -- tests
-> ['git', 'diff', '--stat', 'tree/t1', 'HEAD', '--', 'tests']
-> $ git diff --stat tree/t1 HEAD -- tests
-> applied to all worktrees that match the default pattern of "output/*"

$ agro diff -- tests
-> ['git', 'diff', 'tree/t1', 'HEAD', '--', 'tests']
-> $ git diff tree/t1 HEAD -- tests
-> applied to all worktrees that match the default pattern of "output/*"

agro diff --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees that match the default pattern of "output/*"

agro diff output/mything --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees that match the pattern of "output/mything*"

agro diff output/mything.{3,4} --stat
-> ['git', 'diff', 'tree/t1', 'HEAD', '--stat']
-> $ git diff tree/t1 HEAD --stat
-> applied to all worktrees of branches "output/mything.3", "output/mything.4"

Make it work for all these tests cases both.

Refactor test cases as nec and add new tests for this functionality.