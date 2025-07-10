when the user uncomments the AGENT_CONFIG.gemini.timeout  in their conf.yml, this overrides the -y param being passed to the gemini. refactor how timeout is configured to be a separate categroy of option for the agent and not have the user setting enabling a timeout indicate that flags passed to the agent should be null or not equal tp the default flags passed to the specific model.

You can use the following example to see the pathological behavior:

user@DESKTOP-1EB4G00:~/dev/agro/agro-demo$ agro -vv exec simple mgemini
Inferred agent type 'gemini' from exec_cmd 'mgemini'
No indices provided. Using next available index: 8

--- Processing worktree for index 8 ---
Attempting to remove existing worktree for index 8 (if any)...
Worktree 'trees/t8' not found or not a valid worktree. Skipping removal.
Running command in '.': $ git show-ref --verify --quiet refs/heads/tree/t8
Branch 'tree/t8' not found. Skipping deletion.
♻️  Cleanup for index 8 complete.

Creating new worktree for index 8...
Running command in '.': $ git rev-parse HEAD
Running command in '.': $ git check-ignore -q ./trees
Creating new worktree 't8' at 'trees/t8' on branch 'tree/t8'...
Running command in '.': $ git worktree add -b tree/t8 trees/t8
Preparing worktree (new branch 'tree/t8')
HEAD is now at 31ad998 yup
Created worktree-specific swap dir: trees/t8/.agswap
Copying .env to trees/t8/.env
Adding worktree overrides to trees/t8/.env
Trying to set up Python environment in trees/t8...
Running command in 'trees/t8': $ uv venv
Running command in 'trees/t8': $ uv sync --quiet

🌴 New worktree created successfully.
   Worktree: trees/t8
   Branch: tree/t8
   API Port: 8008
Copied task file to trees/t8/.agswap/simple.md
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.1
017ac2c7b49d76741d7e6db7cf3b0dec5e84c3cb
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.2
31ad9986dff3003cd199d4b1824eabc2f2362780
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.3
31ad9986dff3003cd199d4b1824eabc2f2362780
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.4
31ad9986dff3003cd199d4b1824eabc2f2362780
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.5
31ad9986dff3003cd199d4b1824eabc2f2362780
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.6
8bb63a610ee71d4783f3a158bdf8c7657b1133df
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.7
c6fb34225cddc57e1d9b7449cb475e17c1cdadd3
Running command in '.': $ git rev-parse --verify --quiet refs/heads/output/simple.8
Running command in 'trees/t8': $ git checkout -b output/simple.8
Switched to a new branch 'output/simple.8'
🌱 Working on new branch: output/simple.8
Launching agent in detached mode from within trees/t8...
Applied timeout of 120 seconds to gemini command
['timeout', '120', 'mgemini'] [('cwd', 'trees/t8'), ('stderr', -2), ('start_new_session', True), ('stdout', <_io.BufferedWriter name='trees/t8/.agswap/agro-exec.log'>), ('stdin', <_io.TextIOWrapper name='trees/t8/.agswap/simple.md' mode='r' encoding='UTF-8'>)]
Spawning auto-commit monitor for worktree trees/t8
Committer PID: 2700182
🏃 Agent for index 8 started successfully.
   Worktree: /home/user/dev/agro/agro-demo/trees/t8
   Task file: /home/user/dev/agro/agro-demo/.agdocs/specs/simple.md
   Branch: output/simple.8
   Agent type: gemini
   Initial commit SHA: 31ad99
   Start time: 2025-07-10 14:32:11
   PID: 2700180 (saved to /home/user/dev/agro/agro-demo/.agdocs/swap/t8.pid)
   Log file: /home/user/dev/agro/agro-demo/trees/t8/.agswap/agro-exec.log
   Task file copy: /home/user/dev/agro/agro-demo/trees/t8/.agswap/simple.md