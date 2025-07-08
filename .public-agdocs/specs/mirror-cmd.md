add an agro mirror command that "mirrors" runs the following shell command:
> rsync -av --delete .agdocs/ .public-agdocs/

suppress shell output by default

- thr purpose here is to allow a git tracking of the spec files, even though .agdocs is considered by default internal and gitignored.

- allow src and target to be configurable based on these directories' config values