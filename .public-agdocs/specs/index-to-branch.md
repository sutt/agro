build a command "agro state" which prints out the branch name (output/xxx.N) connected each existing working tree currently.

Build an internal function that can build up this mapping of the state since we'll need it for future commands and functionality.

On appraoch that should work is running "git status" within each working tree's root (or other git command commands that reveal the current branch name) and parsing the branch name out of it.