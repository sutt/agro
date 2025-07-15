add an optional argument to "agro state" command that accepts glob like patterns for matching against a subset of existing branches: agro state [branch-pattern]

Build a separate internal function that can parse the branch patterns and match against (any existing) branches in the git repo since we'll need it for future commands and functionality.

Pattern matching rules:
- If there is an exact match, select only that branch
- If there is not an exact match, assume the value passed has a * at the end, .e.g "output/myfeat" is interpreted as "output/myfeat*" which matches "output/myfeat.1" and "output/myfeat.2".
- Allow curly braces to be interpreted as multi number selection with either a series of comma separated values:
    - series: "{1-4}" -> {1,2,3,4}
    - indv values: "{2,4}" -> {2,4}
    - so "output/myfeat.{1-3}" is looking to match branches "output/myfeat.1", "output/myfeat.2", "output/myfeat.3"
- Use these rules unless you have a better idea how to do basic parsing matching.
- Add some unit tests for this behavior, and identify any corner cases where there may be ambiguity.
