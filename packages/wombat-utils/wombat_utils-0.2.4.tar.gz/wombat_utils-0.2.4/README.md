# wombat-utils

Utilities made to support my personal development, sort of a "catch all" package

## Structure

```
.
├── .coveragerc - Configure code coverage generation
├── .gitignore - Configure files ignores by git commands
├── .gitlab-ci.yml - Configure our gitlab CI pipeline
├── .pre-commit-config.yaml - Configure our pre-commit for code quality checks
├── .python-version - Set our python version, used for python selection in terminals
├── .vscode - Configure our vscode workspace
│   ├── launch.json - Settings used for debugging/running code
│   └── settings.json - Workspace settings
├── README.md - YOU ARE HERE
├── flake.lock - Stores the state of our nix flake
├── flake.nix - Configure our nix environment
├── pyproject.toml - Our project configuration
├── src - Source code to be packaged with the wheel
│   └── wombat - Namespace folder
│       └── utils - Contains utilities for different types
│           ├── __init__.py
│           ├── dictionary.py - Utilities for dictionaries
│           ├── errors - Utilities for handling or generating errors
│           │   ├── decorators.py - Decorators that help enforce code constraints
│           │   └── exceptions.py - Common Exceptions that can be raised
│           └── files
│               └── search.py - Utilities for searching files
└── uv.lock - Stores our installed python versions
```
