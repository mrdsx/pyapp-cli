# PyApp CLI

## About

PyApp CLI is a powerful tool that makes python project setup painless. With this CLI you can easily scaffold FastAPI, Flask or Django project with all necessary dependencies.

## Supported platforms

The CLI can be run on Ubuntu Linux, but it's not guaranteed the CLI will work on other platforms.

## Get started

Before setting up new project, install Python and appropriate package manager you'll use for your project. PyAPP CLI supports following package managers:

- pip
- poetry
- uv

## How to run

Install uv package manager. Then, run `uvx pyapp-cli@latest init`.

## Params

Since v0.3.0 PyApp CLI supports params, so the CLI won't ask you about some settings. It can be useful when automating project creation.

#### `--verbose` - **boolean**
- default: false
- example: `uvx pyapp-cli init --verbose`

#### `--project-path` - **string**
- default: empty string
- example: `uvx pyapp-cli init --project-path=some-path`

#### `--package-manager` - **literal string ("pip", "poetry" or "uv")**
- default: pip
- example: `uvx pyapp-cli init --package-manager=pip`

#### `--python-version` - **string**
- default: 3.12
- example: `uvx pyapp-cli init --python-version=3.12`

#### `--source-folder` - **string**
- default: root
- example: `uvx pyapp-cli init --source-folder=root`

#### `--framework` - **literal string ("fastapi", "flask" or "django") or None**
- default: None
- example: `uvx pyapp-cli init --framework=fastapi`

#### `--libraries` - **list of strings or None**
- default: None
- example: `uvx pyapp-cli init --libraries=requests --libraries=pydantic`

#### `--no-libraries` - **True or None** (False is not valid option)
- default: None
- example: `uvx pyapp-cli init --no-libraries=True`

Important notice: `--no-libraries` and `libraries` arguments can't be used together. You use either one or none of them.

## Contributing

Feel free to open an issue if you have found a bug, have a feature request or you want to expand list of available libraries/frameworks/package managers. You also can open PR if you wish.
