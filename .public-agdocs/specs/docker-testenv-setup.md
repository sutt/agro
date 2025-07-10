add a feature for tests: launch a docker container that will execute a series of tests of an install of the current agro worktree. This new test env is separate from the existing pytests for cli which can remain pure python.

The idea here is the docker container as linux box with filesystem so we can examine the actual artifacts created when different commands and their variation are run.
One thing this container won't nec have is api_key's to different LLM api endpoints so we shouldn't expect the agent's to perform useful work when invoked. 
- Aider can be mocked by passing the -h flag to agent_args so the full agent process never runs. Or we modify the exec-cmd to use a system built-in as a stub.

the docker should have the following packages available:
- uv (as primary python env)
- git (and setup to be able to commit when this functionality is requested by aider or agro)
- aider-chat (installed as uvtool)
- agro package installed (installed as uvtool)
- a copy of the tests to execute, which will also be in the test/ directory of this repo. the actual tests for agro use should occur in a git repo itself

Create several tests that establish proof of concept
- Check the agro cli works, checks the version
- runs an agro exec
- deletes branches
- an ability to reset the repo