Add the updated files to a markdown table in docs/dev-summary-1.md 
with a row containing:
- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
- the file's size
- only include specs/*

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

Update all 