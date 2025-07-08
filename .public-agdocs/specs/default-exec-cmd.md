Add a new optional arg exec-cmd for exec:
> exec <taskfile> [num-trees] [exec-cmd]
- num-trees will always be an int
- exec-cmd will always be a str (non-int)
- we won't always have num-trees when we have exec-cmd and vice-versa, make the parsing logic handle this with the type distiction given.

also:
- pass the exec-cmd in present to the first line in the command dispatched in exec:
```python
command = [
            "maider.sh",  # <- here
```
instead of using maider.sh as the default, create a config var for this as the default and set in to "aider" as the default. Make sure to add this to the default template.