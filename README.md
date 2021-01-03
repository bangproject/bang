# Bang

Bang is a web framework that aspires to make it easy to create fast and correct web apps.

## Installation

This project uses poetry. To install it you first need to install `poetry` which is available in `pip`, from most package managers, or the (recommended installation)[https://python-poetry.org/docs/#installation].

1. Clone the project with `git clone https://github.com/bangproject/bang.git`.
2. Switch to the directory with `cd bang`.
3. Install in a virtual environment with `poetry install`.

## Development

### pre-commit and poetry scripts

This project uses `pre-commit` to manage some code standards. The easiest way to get started with is to `pip install pre-commit` and then in the project directory `pre-commit install`. That's going to install tools based on what it finds in `.pre-commit-config.yaml`.

The command `poetry run pre_commit` will address some code errors with reformatting. And it will show you other errors that you'll need to tend to manually. This is the same as what will run when you try to commit with `git`. So until your code can normally exit with this command you can't commit.

You can check that your tests pass with `poetry run test`. And you can check the coverage with `poetry run coverage`. Your pull requests should have 100% coverage.

### docker-compose workflow

There's a `docker-compose.yml` in the project root that will build a containerized environment when you run `docker-compose -d --build`. Then with the environment running you can execute commands in the container by referencing `docker-compose exec web [CMD]`.

### Summary

The project has three commands that will help you with your development workflow:

	- `poetry run pre_commit`
	- `poetry run test`
	- `poetry run coverage`

There's a `Dockerfile` and `docker-compose.yml`, so you can bring up a containerized environment with your favorite options on `docker-compose up`. This is configured to serve a web application based on the sample application that's in the `app` file. But you can also execute commands in the container with `docker-compose exec [CONTAINER] [COMMAND]`.

## Usage

### It's not complete, but something works

You can build routes based on paths, methods, and parameters. Everything else is up to how you write the handlers that you'll add.

### Example application

In the file `bang/app.py` there's a sample application that uses the framework. This will give you a clearer picture of how you can structure a demo app. I'll update this section as we add more features.
