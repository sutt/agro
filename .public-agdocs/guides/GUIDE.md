### agro dev 
- use uv to run python and package management: `uv run`, `uv sync`, `uv run pytest`, etc
- when adding or modifying commands or flags to cli, update that in the cli help text (if approriately impactful). Also add tests. If you update the argparse namespace the tests will likely need a refactor which you should implement.
- run the cli pytests before finishing and if they are failing attempt to diagnose and fix the error(s).

### experimental: (do not use currently)
- you can call `agro` at a system-level but this won't reflect the edits you applied
- use `uv run python -m src.agro.cli` to run the package without re-installing via a package manager.
- use the `redeploy` script to apply changes for agro to the full system
- add any additional comments on conventions you find useful to the GUIDE.md file
- add any documentation needed to docs/