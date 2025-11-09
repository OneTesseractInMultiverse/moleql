# Setting Up Pre-Commit Hooks


This page explains how to install and enable the pre-commit hooks after cloning the repository.


**Install Pre-Commit**


Install the tool on your system.


```bash
pip install pre-commit

```

Or with pipx:

```bash
pipx install pre-commit

```

**Enable the Hooks**


Run the following command from the root of the repo:

```bash
pre-commit install

```

This creates the `.git/hooks/pre-commit` script and activates all hooks defined in `.pre-commit-config.yaml`.


**Run All Hooks Once**


You can run every hook on the full codebase.

```bash
pre-commit run --all-files

```

**Confirm It Works**


Make a small commit. The hooks should run before Git completes the commit.
