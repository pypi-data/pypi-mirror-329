# Develop!

This document is targeted at project developers. It helps people to make their
first steps. It also serves as a general entry to development documentation like
tooling configuration and usage.

The development environment should have the following tools:

- [Copier](https://copier.readthedocs.io/en/stable/) for project templating.
- [Just](https://github.com/casey/just) for running self-documenting tasks.
- [Mdformat](https://github.com/hukkin/mdformat) for Markdown formatting.
- [Pre-commit](https://pre-commit.com/) for managing pre-commit hooks.
- [ShellCheck](https://github.com/koalaman/shellcheck) for shell script linting.
- [Shfmt](https://github.com/mvdan/sh) for shell script formatting.
- [Uv](https://docs.astral.sh/uv/) for managing Python and friends.
- Unix-like. Not required by itself, but assumed as the standard.

Technically, uv by itself is already enough to work on the project. The other
stuff is just extra and can also be handled by GitHub Actions.

Common tasks like initialization and runnings tests are covered by and
documented in [`Justfile`](./Justfile). To run a complete suite of tasks, just
invoke `just` without arguments.

This projects supports [Development Containers](https://containers.dev/). Check
out [`.devcontainer/README.md`](./.devcontainer/README.md) for more information.
