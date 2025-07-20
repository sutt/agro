# Agro-builds-Agro pt 6
_July 20, 2025_

We're going to take a look at generating the first version of docs from the source code with an agent. 

_If you're interested in a sneak peak, just check out the current [docs sections](../index.md) now to see what we got._


### The task

[**do-docs-1.md**](../../.public-agdocs/specs/do-docs-1.md)
```markdown
Create 3 - 10 pages of markdown docs for this project.

- Add to the docs/ section
- Structure with an:
    - index page linking to each page - first few pages explaining basic and high-level concepts,
    - some pages documenting sub-commands and details
    - some final pages for other common documentation pages
- Use consistent markdown format thoughout pages
- Use some formatting niceties like warnings sections
- You can add TODO - markers where the documentation team can come in and supply extra info or paste the nec code blocks.
```

Since this is a completely new section in this repo, we're looking to generate solutions to the following:
- **The structure** - how the full content is separated into different pages, and what order it is presented in.
- **The formatting patterns** - what headings, sub-headings, description and example sections look like
- **The actual content** - This includes everything from the explanation of the core program, explanation of external tools (e.g. aider and claude), and how to actually document the commands, arguments, and the bahvior they entail

#### Context Engineering

How can models write documentation for a program that doesn't have any documentation yet? Obviously it has access to the source code which can generate some documentation, but it also has access to some pseudo-documentation in agrparse help arguments, in the tests, and in the readme. 

When first running this task, we were getting lots of hallucinations which turned out to be because the examples presented in the repo's readme were using deprecated commands and arguments. So, the more genral idea here is you can create a spec but not launch agents on it until you clean the workspace to have the right context.


### Look at the Solutions

We ran this prompt on five agents:
- **`.1 - .2`:** aider with gemini-2.5-pro 
- **`.3 - .4`:** claude code with sonnet 4
- **`.5`:** gemini-cli with gemin-2.5-pro

Below show the diff totals for what was generated. We can see that gemini models generated around ~400 lines of documentation in each of its respective solutions and claude sonnet produced ~4,000 lines of documentation in each of its respective solutions.

```
--- Running command in t1 (output/do-docs-1.1) ---
$ git show --stat HEAD
commit aedcd6eb516c35211ad54906f8572fb194660216
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:05:02 2025 -0400

    docs: add initial project documentation

 docs/command-reference.md | 140 ++++++++++++++++++++++++++++++++++++++++++++++
 docs/configuration.md     |  28 ++++++++++
 docs/contributing.md      |  46 +++++++++++++++
 docs/core-concepts.md     |  46 +++++++++++++++
 docs/getting-started.md   |  30 ++++++++++
 docs/index.md             |  14 +++++
 6 files changed, 304 insertions(+)

--- Running command in t2 (output/do-docs-1.2) ---
$ git show --stat HEAD
commit 11364b1aac0f3596ed28fde152d185bd69a68167
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:05:57 2025 -0400

    docs: add initial project documentation

 docs/contributing.md            |  54 +++++++++++++++
 docs/getting-started.md         |  72 ++++++++++++++++++++
 docs/guides/basic-workflow.md   |  79 ++++++++++++++++++++++
 docs/index.md                   |  21 ++++++
 docs/introduction.md            |  28 ++++++++
 docs/reference/cli.md           | 142 ++++++++++++++++++++++++++++++++++++++++
 docs/reference/configuration.md |  41 ++++++++++++
 7 files changed, 437 insertions(+)

--- Running command in t3 (output/do-docs-1.3) ---
$ git show --stat HEAD
commit 98286149549c32a8325442366a8f1ffde2ff0357
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:13:05 2025 -0400

    feat: impl do-docs-1 with claude (agro auto-commit)

 docs/agents.md          |  424 ++++++++++++++++++++
 docs/commands.md        |  536 +++++++++++++++++++++++++
 docs/configuration.md   |  439 ++++++++++++++++++++
 docs/contributing.md    |  534 +++++++++++++++++++++++++
 docs/core-concepts.md   |  339 ++++++++++++++++
 docs/examples.md        | 1020 +++++++++++++++++++++++++++++++++++++++++++++++
 docs/getting-started.md |  242 +++++++++++
 docs/index.md           |   93 +++++
 docs/troubleshooting.md |  708 ++++++++++++++++++++++++++++++++
 docs/workflows.md       |  495 +++++++++++++++++++++++
 10 files changed, 4830 insertions(+)

--- Running command in t4 (output/do-docs-1.4) ---
$ git show --stat HEAD
commit 2d425b71eb5ac15562a5fbc25902b5958b2d1dcf
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:11:06 2025 -0400

    feat: impl do-docs-1 with claude (agro auto-commit)

 docs/agents.md          | 487 +++++++++++++++++++++++++++++++++++++++
 docs/commands.md        | 380 +++++++++++++++++++++++++++++++
 docs/concepts.md        | 281 +++++++++++++++++++++++
 docs/configuration.md   | 460 +++++++++++++++++++++++++++++++++++++
 docs/contributing.md    | 502 +++++++++++++++++++++++++++++++++++++++++
 docs/faq.md             | 504 +++++++++++++++++++++++++++++++++++++++++
 docs/getting-started.md | 170 ++++++++++++++
 docs/index.md           |  76 +++++++
 docs/troubleshooting.md | 587 ++++++++++++++++++++++++++++++++++++++++++++++++
 docs/workflows.md       | 478 +++++++++++++++++++++++++++++++++++++++
 10 files changed, 3925 insertions(+)

--- Running command in t5 (output/do-docs-1.5) ---
$ git show --stat HEAD
commit 50bc72c7951c487fd77b1587fdb29fed4a6eea3d
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:04:58 2025 -0400

    feat: impl do-docs-1 with gemini (agro auto-commit)

 docs/commands.md        | 164 ++++++++++++++++++++++++++++++++++++++++++++++++
 docs/concepts.md        |  40 ++++++++++++
 docs/configuration.md   |  92 +++++++++++++++++++++++++++
 docs/contributing.md    |  54 ++++++++++++++++
 docs/faq.md             |  34 ++++++++++
 docs/getting-started.md |  86 +++++++++++++++++++++++++
 docs/index.md           |  17 +++++
 7 files changed, 487 insertions(+)
```

### Accepting & Correcting
 
We ultimately went with solution that claude generated [`98286`](https://github.com/sutt/agro/commit/98286149549c32a8325442366a8f1ffde2ff0357).


And then large-scale and small-scale changes on-top of this in [`a62f61`](https://github.com/sutt/agro/commit/a62f615878085dedcc1bfccd95bb075abc536200). Below we'll take a look at the corrections to see what was both good and bad about the documentation generated by claude.

**Initial Generation:**
```
commit 98286149549c32a8325442366a8f1ffde2ff0357
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 14:13:05 2025 -0400

    feat: impl do-docs-1 with claude (agro auto-commit)

 docs/agents.md          |  424 ++++++++++++++++++++
 docs/commands.md        |  536 +++++++++++++++++++++++++
 docs/configuration.md   |  439 ++++++++++++++++++++
 docs/contributing.md    |  534 +++++++++++++++++++++++++
 docs/core-concepts.md   |  339 ++++++++++++++++
 docs/examples.md        | 1020 +++++++++++++++++++++++++++++++++++++++++++++++
 docs/getting-started.md |  242 +++++++++++
 docs/index.md           |   93 +++++
 docs/troubleshooting.md |  708 ++++++++++++++++++++++++++++++++
 docs/workflows.md       |  495 +++++++++++++++++++++++
 10 files changed, 4830 insertions(+)
```
**Manual Correction (so far):**
```
commit a62f615878085dedcc1bfccd95bb075abc536200
Author: sutt <wsutton17@gmail.com>
Date:   Fri Jul 18 20:44:45 2025 -0400

    docs: major refinements on ai-generated docs

 docs/agents.md          | 311 +++---------------------------------
 docs/commands.md        |  65 +++-----
 docs/configuration.md   | 414 ++++++------------------------------------------
 docs/contributing.md    |   2 +
 docs/core-concepts.md   | 189 +++++++++++-----------
 docs/examples.md        |   2 +
 docs/getting-started.md |  74 ++++-----
 docs/index.md           |  29 ++--
 docs/troubleshooting.md |   2 +
 docs/workflows.md       |   2 +
 10 files changed, 240 insertions(+), 850 deletions(-)
```


### What needed to be corrected

#### Agro-specific
- The <branch-pattern> cli-arguments were being shown in examples as enclosed in single quotes, which is something we don't need. But
- Configuration section was completely off for variable naming and structure often using more traditional lower case variable, whereas agro.conf.yml actually uses ENV_VAR-like all uppercase with underscore style variables. Ideally agro should use the style that calude hallucinates here.
- Didn't really understand the `mirror` command
- Hallucinated a hierarchy of config files that load (system, user, project) when really only project-level configs currently exist. 
    - This is something that seems to occur often, that if a tool you are building
- We needed to add some additional tips like agro exec called without task-file runs the most recently modified taskfile. This wasn't "documented" anywhere, but the logic did exist.
- Seemed to overemphasize the agro state command, which is currently not too important or useful.
- Didn't really understand the mapping of worktree indexes to output branch indexes (once again agents excel at documenting the most likely pattern, even if it's wrong)

#### Non-Agro stuff
- How to install agents like claude code and aider
- CLI flags for the individual models
- Configuration of the models, espcially around the idea of agro enabling `auto_commit` or api key variables.
- Ultimately we punted on fixing four whole sections: workflows, example, troubleshooting, 
- Went off on a tangent on the taskfiles: looks like the advice it gave is the more traditional way of prompting spec files used in the ai-agents community, currently used for the likes of kiro and cursor.

#### Overall Summary 
- Overall: agents are very good at collating the shallow information that is documented in a distributed fashion across the project, but bad at digging deep / reasoning about edge behavior. They are also bad enough to be unuseful about supplying the supplementary information on the 
- Overall: agents, especially claude tend to produce documentation that is interpolated as the "average" piece of software in the category. This seems to be the source of the hallucinations: not that they are wildly wrong, but more good intuition of documenting features that should exist in the most best-practices form.

### What it did well

- Provided nice formatting
    - Full sturcture of how the docs should be layed out
    - One excellent thing claude's solutions did which is nice is adds a "next section" footer to each page which is great for UX / navigation.
    - Added formatting niceties like a block quote with emoji for a small "Tip section" we can insert other places in the docs.
- Kept examples short and to the point

### Next Steps

It will be interesting to see what having this information in the code repo to supplement prompts like an `llm.txt` / `llm-full.txt`.

It will be interesting to see the next round of document generation when we add or modify features iv `v0.1.7` to see if it can map those changes into the docs.