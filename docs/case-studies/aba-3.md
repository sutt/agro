# Agro-builds-Agro pt 3
_July 14, 2025_

In this article, let's take a look at using agents to produce for **documentation based tasks** like creating [changelogs](../CHANGELOG.md) from diffs and generating summaries of the prompts and solutions into a [dev summary](../dev-summary-v1.md)

## Generating changelogs

Here we can simply get a full git diff into the verbiage of the spec:
- We'll use the handy version tags
- We'll use this `:(exclude)<dir>` arguments to keep the AI focused on actual source code, not the specs and docs.

```
 git diff v0.1.5 v0.1.5 -- . ':(exclude).public-agdocs' ':(exclude)docs' > .agdocs/specs/changelog-1.6.md
```

Now we'll just add some guidance

[**changelog-1.6md**](../../.public-agdocs/specs/changelog-1.6.md)
>Below is a diff from v0.1.5 to v0.1.6.
Add entries to docs/CHANGELOG.md to describe the change
diff --git a/src/agro/cli.py b/src/agro/cli.py
index 238ad6c..fd19fc6 100644
--- a/src/agro/cli.py
+++ b/src/agro/cli.py
@@ -40,10 +40,6 @@ def _dispatch_exec(args):
                 raise ValueError(
                     "Number of trees specified twice (e.g. positionally and with -n)."
                 )
...

Trying with each agent type, it looks like **claude** really shined on this one. The other agents weren't bad but didn't keep the base structure of the changelog supplied to them. 

Had I wanted to spend more time on this activity, I think I may have done some iteration to find the changelog formatted that fit this project best, but for now we'll keep it simple.

## Generating dev summaries

Beyond the classic changelog, we can also produce a detailed summary

- v1: Let's convert a git printout to markdown table with file linking
    - benefit
- v2: Let's give a preview of the content and sort them
- v3: Get the AI to map the 

After going through these versions we'll produce something like this (the whole table you can see [here](../dev-summary-v1.md))

| Task File | Contents (truncated) | Accepted SHA | Non-test Diffs | Test Diffs |
|------|-------------|---------|-------------|------------|
| [clean-help.md](../.public-agdocs/specs/clean-help.md) | tasks: - drop support the for the flag: agro exec -t - update help for agro cli: - document agro state command - document -a option to exec | [8990066](https://github.com/sutt/agro/commit/8990066) | +19/-15 | +0/-0 |
| [fade-pattern.md](../.public-agdocs/specs/fade-pattern.md) | apply the same branch pattern matching logic to the <pattern> arg in "agro fade" as is used in surrender and muster. fix any tests as nec. | [2cacd2e](https://github.com/sutt/agro/commit/2cacd2e) | +27/-8 | +122/-11 |
| [gemini-guide.md](../.public-agdocs/specs/gemini-guide.md) | when launching a gemini agent from exec: - check if a .gemini directory exists in at the root of the git worktree when you go to launch | [b01a152](https://github.com/sutt/agro/commit/b01a152) | +22/-0 | +0/-0 |


#### V1

This time we're using this command to add info our spec file: ```git diff --stat v0.1.5 v0.1.6 -- .public-agdocs/``` where we're chosing only the mirrored spec files.

Here we're just checking that agents are able to convert into markdown and do relative linking appropriately within this repo. It works 👍.

[summary-1.md](../../.public-agdocs/specs/summary-1.md)

>Add the updated files to a markdown table in docs/dev-summary-1.md 
with a row containing:
>- just the filename and have it be linked with relative path notation to where it resides in .public-agdocs
>- the file's size
>- only include specs/*
>Here's the result for the following command:
>git diff --stat v0.1.5 v0.1.6 -- .public-agdocs/
 .public-agdocs/conf/agro.conf.yml           |    2 +-
 .public-agdocs/guides/GUIDE.md              |   11 +
 .public-agdocs/specs/branch-patterns.md     |   13 +
 ...

#### V2

We're extending the what we did in v1 but:
- Sorting the specs in the order they were created/implemented. Unfortunately the spec files all have the same creation date (because they are rsync'd all at the same right before each release) so we won't be able to figure out the order this. But they are saved in my gitignored .agdocs (from whence they're mirrored) therefore I'll add that information.
- Adding the contents of the specs itself.

Can the agent merge those additional information with the existing table it built? Turns out it does it perfectly 👍.

[summary-2.md](../../.public-agdocs/specs/summary-2.md)

>...
ls -lt .agdocs/specs/ 
-rw-r--r-- 1 user user  1600 Jul 15 18:56 summary-2.md
-rw-r--r-- 1 user user  1312 Jul 15 18:48 summary-1.md
-rw-r--r-- 1 user user 28032 Jul 15 17:05 changelog-1.5.md
-rw-r--r-- 1 user user 43370 Jul 15 16:52 changelog-1.6.md
-rw-r--r-- 1 user user   166 Jul 15 15:34 clean-help.md
...

#### V3

Here's where it gets pretty cool, we'll ask the agent to perform a fuzzy match between the spec file and the commit message. We'll provide it the git log with messages and asking the agent to 

Does it work? Spot-checking looks good, including recognizing `do-docs-1` was not implemented. The one caveat I'd have with the agents results is crediting one commit to two different specs (`commit-after` & `commit-after-v2`).

[summary-3.md](../../.public-agdocs/specs/summary-3.md)
> add a field that links to a 6-char git sha entry  on the github repo: github.com/sutt/agro. Do your best guess to find the corresponding commit (available with commit message below). If your guess is too uncertain, or it appears there is no commit for it, place an n/a for this entry.


