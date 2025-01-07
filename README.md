# python-project-template

Python project template built using uv, which is an extremely fast Python package and project manager, written in Rust. It aims to simplify project setup, streamline dependency management, and promote best practices for Python development

## Dependencies

Uv is a single command line executable. There are a number of ways to install it, but the easiest is to use the provided installation script:

```<sh>
curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.local/bin/env
```

You can add dependencies to your `pyproject.toml` with the uv add command. 

```console
# Specify a version constraint
uv add 'requests==2.31.0'

# Add a git dependency
uv add git+https://github.com/psf/requests
```

To remove a package, you can use uv remove:

```console
uv remove requests
```

## How to use it?

You can execute your scripts using `uv run`:

```console
$ uv run project-template/hello.py 
Hello world
```

## Using Makefile for Common Tasks

This project includes a Makefile to automate common tasks like linting, type checking, and running the application. You can execute the following commands with make:

### Install dependencies and create a virtual environment:

```console
$ make install
```
### Run linting (Ruff) and type checking (MyPy):

```console
$ make check
```
### Run the application after performing linting and type checking:

```console
$ make run
```

The make commands will ensure that the code follows best practices and is checked for errors before running.
