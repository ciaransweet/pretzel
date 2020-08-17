# pretzel 🥨☁️ ![Master Status](https://github.com/ciaranevans/pretzel/workflows/CI/badge.svg?branch=master)

_An AWS Serverless application within a monorepo_

---

The idea behind `pretzel` is to try and provide an example of a AWS hosted serverless application that is contained within a monorepo.

`pretzel` will comprise of automated builds, tests, and deployments.

CI/CD is handled with GitHub Actions - [Found here](https://github.com/ciaranevans/pretzel/actions)


_The name Pretzel was decided when A: I renamed it from MoSeX (Monorepo Serverless eXample) and B: when I found this gif:_

![Pretzel Making Bot](https://media.giphy.com/media/bwmYGtDbRCJyg/giphy-downsized.gif)

# Development - Setup and useful commands

<details>
<summary><b>Dependencies</b></summary>

**Python 3.8+** I recommend using [pyenv](https://github.com/pyenv/pyenv)

**Node Version Manager** [Found here](https://github.com/nvm-sh/nvm)

**Pipenv** [Found here](https://github.com/pypa/pipenv)

To ensure that Pipenv uses your pyenv Python install:
```bash
export PYENV_ROOT=<root/to/pyenv/install>
export PIPENV_PYTHON=$PYENV_ROOT/shims/python
```

**AWS CLI** [Found here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

**AWS CDK**

```bash
$ npm install -g aws-cdk
```

**An .env file**

```bash
$ cat .env
ENV=my-dev-env
```
</details>

<details>
<summary><b>Setup commands</b></summary>
Before you can develop, make sure you've run:

```bash
$ nvm install # To setup Node and use the correct version
$ pipenv install -d # To initialise the pipenv virtual environment and install the project dependencies
$ aws configure # To setup the AWS CLI
```
</details>

<details>
<summary><b>Makefile</b></summary>

**`make lint`**

> This will perform a dry run of `flake8`, `isort`, and `black` and let you know what issues were found

**`make format`**

> This will perform a run of `isort` and `black`, this **will** modify files if issues were found

**`make unit`**

> This will use `pytest` to run all unit tests found within `tests/unit`

**`make integration`**

> This will use `pytest` to run all integration tests found within `tests/integration`

**`make diff`**

> This will run a `cdk diff` using the value of `ENV` in your `.env` file to determine if there are any changes between your local stack definition and that of the the deployed instance (There may not be one, so everything will be new)

**`make deploy`**

> This will run a `cdk deploy` using the value of `ENV` in your `.env` file to deploy your local stack definition to AWS

**`make destroy`**

> This will run a `cdk destroy` using the value of `ENV` in your `.env` file to destroy your deployed stack

### Makefile combos

**`make format unit`**

> This will catch little formatting errors that are annoying to find out about when waiting for CI builds. It will also ensure that your tests pass and there's no silly mistakes laying around!

**`make deploy integration destroy`**
> This will deploy the environment, run the tests then destroy it.
</details>
