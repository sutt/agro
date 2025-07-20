# Agro-builds-Agro pt 4
_July 15, 2025_

In this part, let's ask what type of human-intelligence / skill can be involved when doing ai-generated-first code bases.

Obviously we're trying to achieve momentum and cadence around task creation, solution-generation, review and merge. But when does slowing down and thinking come into play? How about during the consideration of UX. Here's a following scenario:

## Considering the Task

At `v0.1.6` we're now trying to clean up some commands in agro. 

To consider is:
- We've refactored fade, muster and surrender to use branch-pattern glob-like inputs/
- We've got user experience of how the commands commonly get used to build the last few version. What we see is...

Currently each round of iterations leaves us with many misc branches and worktrees to be cleaned up. That's currently accomplished by running:

```bash
agro delete --all  # delete all worktrees
# run after delete
agro fade output/   # delete all branches starting with "output/" 
```

This is not ideal because `agro delete` will be moved to `agro tree delete` and the `--all` flag is a bit awkward for a common invokation. And the idea of having to run two specialty commands for a common action is less than completely ergonomic.

But there is some **flexibility that's nice** about breaking up the action into two commands: Eliminating the trees removes the replicated environment which allows the agents to run commands and tests in parallel and isolation which is essential while agents are running and generating code. But not essentail (or can be reconstructed) after they finish. However the branch itself contains the generated code, which we may be saving for review of reference later. So we'd like the user to be able to clean up the tree, without deleting the branch

So, how could we make one command with the power of both these concepts, while still allowing some flexibility: the desired flexibili

### Solutions

Given these contraints and requests we come up with.

```
agro clean [--soft] [branch-pattern]
    default: --hard
    if branch-pattern is null, default: output/ (more specificlly: config.WORKTREE_OUTPUT_BRANCH_PREFIX)
```
- `--soft` will delete just the worktree
- `--hard` will delete the worktree and the branch

This will give us:
- an easy to run command by default: `agro clean` which will handle everything we want, with switchability for the 10-20% of the time you want to do something different.

### Conclusion

This is just one example of how understanding your product / understanding how users use it, will help you steer the prompt in a valuable direction, more so than the ai could ever on its own.

---

## Navigation

- [← Previous: ABA-3 - Documentation Generation with AI](aba-3.md)
- [Case Studies Index](index.md)
- [Next: ABA-5 - YOLO Mode and Command Execution →](aba-5.md)

