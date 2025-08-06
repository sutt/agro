# Agro builds Vidster
_July 23, 2025_

Vidster is an a cli client for generating videos with Google's gemini / vertex api's via the Veo2/3 model, available [here](https://github.com/sutt/vidstr).

We'll take a look at using Agro to build this client app which has some elements similiar to Agro like cli and some different elements, like needing to use non standard-lib packages, some of them popular and old like `opencv` and some of them relatively new like `google-genai`.

To see how the first day looked from a prompt-and-solution overview, checkout the project's agro-generated [DevLog](https://github.com/sutt/vidstr/blob/master/docs/dev-log-v1.md).

### Setup

Unlike Agro which got ported from half dozen functions in an existing shell script, Vidster started with a copy of their documentation in a `demo.py` file and started being built from task files.

Immediately it was clear that the coding agents were struggling with implementing this, even when being supplied documentation examples pasted into the task files.

### Using external documentation

A docfile for `google-genai` package was added to the agro guides in `.agdocs/guides/`. This gave every agent a read-only copy of this file within its startup prompt. In addition, within `GUIDE.md` there were documentation urls for the pacakge:

[GUIDE.md](https://github.com/sutt/vidstr/blob/master/.public-agdocs/guides/GUIDE.md)
```markdown
### client api documentation
- there is a copy of the readme from the github project for the package (https://raw.githubusercontent.com/googleapis/python-genai/refs/heads/main/README.md) in python-genai.md,
- additional documentation is available on the web at:
    - https://googleapis.github.io/python-genai/index.html
    - https://googleapis.github.io/python-genai/genai.html
    - https://github.com/googleapis/python-genai
```

It was tricky to find the right level of documentation to supply the agents as a file. On the one hand the full html docs were too long and heavily formatted with html and the quickstart html docs didn't have the level of detail for the few methods we're concerned with to make the coding agents impervious against mistakes in utilizing this the google genai package.

The compromise was using the README file from the github repo of the package which has extensive examples. It would be interesting to what an `llms.txt` looks like for this package.

As opposed to difficulties of using google-genai, the agents were able to use `python-opencv` well for a very standard problem of extrating a frame from a mp4. The success likely owes that it is because the package is old and popular and has many examples of dos and donts in the training. 

So the issue is how to get documentation in the context to the agents, and more generally and preferably have the agents configured or guided in such a way. This led me to develop an experiment to look into how to do this in the future.


### Experiment

After seeing the stuggles, it was the perfect test case, I decided to combine with the existing simple tutorial for agro of the fastapi server. You can get this new test repo here: https://github.com/sutt/demo-agro-ext-lib


#### Setup

We dispatch four differently configured agents - two aider, two claude - on the same task.

Agent1 - aider, not YOLO mode
Agent2 - aider, YOLO mode (can run any command)
Agent3 - claude code, in non-YOLO mode
Agent4 - claude code, YOLO mode (can run any command) 

We ask two questions:
- *Do yolo mode runs install packages?* **(Answer: no, for both agents)**
- *Do agents scrape the documentation urls?* **(Answer: no for claude, yes for aider)**

Clearly, the answers we get here show our agents are running sub-optimally. 

But with some experimentation we genrate configs / guides we fix these problems: we get both claude and aider to scrape and execute bash commands...

#### Variation:

For this succesful refactor, we do two things:
 - add encouragemnt for agentic beahvior (run commands, search web) to the GUIDE.md file which is passed to the agents.
 - we added `--dangerously-skip-permissions` to agent args for claude. Even though we were passing `"--allowedTools", "Write Edit MultiEdit WebFetch WebSearch Bash"` it didn't seem to allow these more advanced commands to run. **(Update: after re-testing this is no longer true, dangerous mode is not required to get WebFetch tool use.)**


The **GUIDE.md** was augmented to:
```diff
+# Demo-Server Project
+
+Guidance for coding agents:
+- if any documentation urls are provided, make sure to scrape those to obtain information on the package.
+- run package installation commands if changing any packages.
+- bash scripts to verify your work.
+- get documentation on 3rd party packages by running something like: uv run python -c "import foo; print(help(foo.bar))"
+- you continue to run commands and search the web until you have succeeded at your task.
+
+Best practices for coding agents:
+- Use uv for running the app and package management.
+- use `uv run pytest` to run pytest.
+- when adding new packages to pyproject.toml, make sure to update the environment with `uv sync --all-extras`
+- add any nec packages to main dependencies and/or to the testing group dependencies if you write tests that need those.

```

This variation can be obtained from **experiment/v2** branch on the repo like this:

```bash
# get the different branch that has new guide
git fetch origin experiment/v2:experiment:v2
git checkout experiment/v2
# copy guide into active position
cp .public-agdocs/guides/GUIDE.md .agdocs/guides/GUIDE.md
```

#### Scrape: Aider ✅
Success comes initially, looking into the logs from the agent, we see in does fetch the documentation in `.aider.chat.history.md` in the agent's worktree at `trees/tN`:

```md
> Add file to the chat? (Y)es/(N)o/(D)on't ask again [Yes]: y  
> https://github.com/googleapis/python-genai  
> Add URL to the chat? (Y)es/(N)o/(A)ll/(S)kip all/(D)on't ask again [Yes]: y  
> Scraping https://github.com/googleapis/python-genai...  
> https://googleapis.github.io/python-genai/  
> Add URL to the chat? (Y)es/(N)o/(A)ll/(S)kip all/(D)on't ask again [Yes]: y  
> Scraping https://googleapis.github.io/python-genai/...  
```

#### Scrape: Claude ✅
Initially there were no instances of "WebFetch" in the claude debug logs, which are available in `trees/t<index>/.agswap/agro-exec.log` but now we can see the calls to the tool are present.
```
[DEBUG] executePreToolHooks called for tool: WebFetch
[DEBUG] Executing hooks for PreToolUse:WebFetch
[DEBUG] Getting matching hook commands for PreToolUse with query: WebFetch
[DEBUG] Found 0 hook matchers in settings
[DEBUG] Matched 0 unique hooks for query "WebFetch" (0 before deduplication)
[DEBUG] Found 0 hook commands to execute
[DEBUG] executePreToolHooks called for tool: WebFetch
[DEBUG] Executing hooks for PreToolUse:WebFetch
[DEBUG] Getting matching hook commands for PreToolUse with query: WebFetch
```

#### uv sync: Aider ✅

cd-ing into the agent's workspace we can run `uv pip list` and see that google-genai is installed in the environment.

It's important to do this before running pytest or `agro muster -c testq` since those invokation will cause uv to self install the new packages added to the venv

#### uv sync: Claude ✅

(Same process as for aider)

We can also see **uv.lock** was modified showing that `uv sync` was likely executed.


### Results

The best of the first version was Agent2 (**aider in YOLO mode**) which had a solution which worked when a valid api key was added. And the tests all passed after some manual intervention of:
```bash
uv sync --all-extras # was missing pytest but did install google-generativeai
uv pip install pytest-asyncio # helps the one failing b/c it added a pytest.mark
```

One of the problems that aider faced was donwloading the wrong package from pypi, `google-generativeai` instead of `google-genai`. This is something claude got right. This is a strange error since aider did scrape the docs

The best of the second version of the experiment was **claude in dangerously-skip-permissions** mode which genrated a perfect turn-key solution, and had all tests pass on the initial mode. That solution can be seen on branch solution/agent.4 here: [`7f30dc`](https://github.com/sutt/demo-agro-ext-lib/commit/7f30dc2960bf263f38697f006eb639a563a9af5a)


#### Solutions Summary

This was generated by:

```
agro muster -c fulldiffout output/genai-call.{1-4}
```

where `fulldiffout` is in the agro config as:

```yaml
MUSTER_COMMON_CMDS:
  fulldiffout: "(echo \"#====== pwd: $(pwd)\"; git diff master HEAD)  >> /home/wsutt/dev/pkgs/agro/demo-ext-lib/full.diff"
```

Now copy `full.diff` file that has been created into .agdocs/specs add some extra explanation at the top to explain the task, then `agro exec` on the task: 

**summary-1.md**
>Generate a markdown table in a new file ./results.md summarizing the following information multiple solutions to a coding task by separate coding agents.
For each of the solutions provided answer the following:
>- what were  api key(s) added
>- what were the packages added
>- what was the main method implemented to call the img gen api
>- how many test, and what did they test for.
>...

Running `agro exec` on that task file now generates this:

| Solution | API Key(s) Added | Packages Added | Main Method Implemented | Tests Added |
| :--- | :--- | :--- | :--- | :--- |
| **t1** | `GEMINI_API_KEY` | `google-generativeai`, `Pillow` | `client.models.generate_images(...)` (sync) | 2 tests: success case (mocking `genai.Client` and returning a real image), and missing API key case. |
| **t2** | `GEMINI_API_KEY` | `google-generativeai` | `await client.aio.models.generate_images(...)` (async) | 2 tests: success case (mocking module-level client with `AsyncMock`), and missing API key case. |
| **t3** | `GOOGLE_API_KEY` | `google-genai`, `Pillow`, `pytest-mock` | `genai.generate_images(...)` (sync) | 5 tests, including success (image returned), missing API key, and API error. Some tests appear inconsistent with the final implementation. |
| **t4** | `GOOGLE_API_KEY` | `google-genai` | `model.generate_content(...)` (sync) | 3 tests for success, custom prompt, and API failure. **This solution does not generate an image, it returns a JSON response.** |

---

### Footnotes

- [other solution summary tables](./assets/other-summaries.md)

## Navigation

- [← Previous: ABA-6 - Docs Generation with AI](aba-6.md)
- [Case Studies Index](index.md)
- [Next: Vidstr-2 - External Packages + Agentic Commands →](aba-vidstr-2.md)