Add the updated files to a markdown table in docs/dev-summary-v1.md 
with a row containing:
- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
- a truncated (max 150 chars) listing of the files contents
- add a field which be a placeholder for now: it will link to a 6-char git sha entry (you can use ffffff as a placeholder ) on the github repo.

Rules for the table:
- only include specs/* files for rows
- sort by date order desc (the date information will supplied at the end)



Here's the result for the following command:

git diff --stat v0.1.5 v0.1.6 -- .public-agdocs/

 .public-agdocs/conf/agro.conf.yml           |    2 +-
 .public-agdocs/guides/GUIDE.md              |   11 +
 .public-agdocs/specs/branch-patterns.md     |   13 +
 .public-agdocs/specs/changelog-1.5.md       |  848 ++++++++++++++++++++
 .public-agdocs/specs/changelog-1.6.md       | 1141 +++++++++++++++++++++++++++
 .public-agdocs/specs/clean-help.md          |    7 +
 .public-agdocs/specs/clean-indices.md       |    4 +
 .public-agdocs/specs/do-docs-1.md           |   10 +
 .public-agdocs/specs/fade-pattern.md        |    2 +
 .public-agdocs/specs/fixup-1.md             |   36 +
 .public-agdocs/specs/gemini-guide.md        |   17 +
 .public-agdocs/specs/guide-files.md         |   11 +
 .public-agdocs/specs/index-to-branch.md     |    5 +
 .public-agdocs/specs/indices-to-branches.md |   11 +
 .public-agdocs/specs/muster-brachname.md    |    4 +
 .public-agdocs/specs/muster-vv.md           |    3 +
 16 files changed, 2124 insertions(+), 1 deletion(-)

Here's the information for the date created which should be used to sort the rows for the table above.

Results of the command: 

ls -lt .agdocs/specs/ 


total 412
-rw-r--r-- 1 user user  1600 Jul 15 18:56 summary-2.md
-rw-r--r-- 1 user user  1312 Jul 15 18:48 summary-1.md
-rw-r--r-- 1 user user 28032 Jul 15 17:05 changelog-1.5.md
-rw-r--r-- 1 user user 43370 Jul 15 16:52 changelog-1.6.md
-rw-r--r-- 1 user user   166 Jul 15 15:34 clean-help.md
-rw-r--r-- 1 user user   138 Jul 15 15:31 fade-pattern.md
-rw-r--r-- 1 user user   805 Jul 15 15:28 gemini-guide.md
-rw-r--r-- 1 user user   184 Jul 15 12:39 muster-brachname.md
-rw-r--r-- 1 user user   567 Jul 15 12:35 muster-vv.md
-rw-r--r-- 1 user user   173 Jul 15 11:01 clean-indices.md
-rw-r--r-- 1 user user   407 Jul 15 10:57 indices-to-branches.md
-rw-r--r-- 1 user user  1119 Jul 15 10:08 fixup-1.md
-rw-r--r-- 1 user user  1100 Jul 15 09:08 branch-patterns.md
-rw-r--r-- 1 user user   448 Jul 15 08:39 index-to-branch.md
-rw-r--r-- 1 user user   810 Jul 14 18:56 guide-files.md
-rw-r--r-- 1 user user   541 Jul 14 18:28 do-docs-1.md
