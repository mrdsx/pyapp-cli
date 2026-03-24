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

Use `main.py init` command to run the CLI:

```bash
python main.py init              # python interpreter
poetry run python main.py init   # poetry
uv run main.py init              # uv
```

Alertnatively, you can use python3 prefix when running command.

## Contributing

Feel free to open an issue if you have found a bug, have a feature request or you want to expand list of available libraries/frameworks/package managers. You also can open PR if you wish.
