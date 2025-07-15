Below are bash output for various commands:

We can see that:
- works: agro state output/index-to-branch.{1-2}
- fails: agro state output/index-to-branch.{1,2}
- works: agro 'state output/index-to-branch.{1,2}'

Can the fail case be made to work so we don't have to use quotes for the branch pattern?


user@DESKTOP-1EB4G00:~/dev/agro/agro$ git branch
  feat/onesix
  master
+ output/branch-patterns.1
+ output/branch-patterns.2
* output/branch-patterns.2.copy
  output/do-docs-1.1
  output/do-docs-1.2
  output/do-docs-1.3
+ output/index-to-branch.1
  output/index-to-branch.1.copy
+ output/index-to-branch.2
  remote/onesix
  tree/t3
  tree/t4
  tree/t5
  tree/t6
user@DESKTOP-1EB4G00:~/dev/agro/agro$ agro state output/index-to-branch.{1-2}
t3: output/index-to-branch.1
t4: output/index-to-branch.2
user@DESKTOP-1EB4G00:~/dev/agro/agro$ agro state output/index-to-branch.{1,2}
usage: agro [-h] [--version] [-v] [-q]
agro: error: unrecognized arguments: output/index-to-branch.2
user@DESKTOP-1EB4G00:~/dev/agro/agro$ agro state 'output/index-to-branch.{1,2}'
t3: output/index-to-branch.1
t4: output/index-to-branch.2
