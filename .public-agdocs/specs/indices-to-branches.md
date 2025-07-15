refactor the following commands to use branch-patterns for an arg instead of index / indices:
- agro surrender
- agro muster

keep the arg optional if it already is, keep it required if it already is.

use the same branch matching pattern logic and functions as for "agro state" command

update the logic to map the branch pattern to tree index then perfrom the same functionality.

update the tests as nec.