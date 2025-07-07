# Package Versioning

This document outlines how versioning is handled for the `agro` package.

## Version Source

The single source of truth for the package version is `pyproject.toml` in the root of the repository.

```toml
[project]
name = "agro"
version = "0.1.0"
...
```

The version is dynamically read from the package metadata at runtime. This means you only need to update `pyproject.toml` when releasing a new version.

## CLI Versioning

The CLI provides a `--version` flag to display the current version:

```sh
agro --version
```

This will output something like `agro 0.1.0`.

## Releasing a New Version

To release a new version of `agro`, follow these steps:

1.  **Update the version in `pyproject.toml`**:
    Increment the `version` number according to [Semantic Versioning](https://semver.org/) principles. For example, change `version = "0.1.0"` to `version = "0.2.0"`.

2.  **Commit the change**:
    ```sh
    git add pyproject.toml
    git commit -m "Bump version to 0.2.0"
    ```

3.  **Tag the release**:
    It's a good practice to tag the commit with the version number.
    ```sh
    git tag -a v0.2.0 -m "Version 0.2.0"
    ```

4.  **Push the commit and tag**:
    ```sh
    git push
    git push --tags
    ```

5.  **Build and publish (e.g., to PyPI)**:
    Use a tool like `build` and `twine` to create the distribution packages and upload them.
    ```sh
    python -m build
    twine upload dist/*
    ```
    Ensure you have the necessary credentials configured for `twine`.
