# Luminary Cloud Python SDK

- [Quickstart](#quickstart) **(recommended)**
- [Manual Installation](#manual-installation)
- [Building the wheel](#building-the-wheel)
- [Generating documentation](#generating-documentation)
- [Configuration](#configuration)
- [Development Guide](#development-guide)

## Quickstart

To start using the SDK (via Python REPL):
```
docker compose run --build sdk
```

![Kapture 2023-03-29 at 14 55 37](https://user-images.githubusercontent.com/6025130/228680101-f6cfea54-07a8-4251-9666-55fb93cedb76.gif)

You only need the `--build` option if you're running for the first time or if
the source has changed.

#### Other useful commands
- `docker compose run sdk sh` to start an interactive shell.
- `docker compose run sdk pytest` to run unit tests.
- `docker compose run sdk python my_script.py` to run an example script.

## Running against a dev environment

From within the `sdk` container, in a Python REPL, do the following to point the SDK to a dev
environment:

```
>>> import luminarycloud as lc
>>> from sdk_util import get_client_for_env
>>> lc.set_default_client(get_client_for_env(env_name="{YOUR_ENV_NAME}"))
```

As with other environments, the first time you try to use your dev environment the SDK will will
print a URL you need to follow to authenticate.

## SDK Releases

To release a new version of the SDK, create a PR with a commit that:
 1. bumps the `version` field in [`python/sdk/setup.cfg`](./setup.cfg),
 2. adds a new release notes file in `python/sdk/docs/source/releases/v{NEW_VERSION}.md`,
 3. adds the new version to the top of the `toctree` in [`python/sdk/docs/source/releases/index.md`](./docs/source/releases/index.md),

Once that PR is merged, the rest happens automatically. First, the
[SDK Auto Tag Release Commits workflow](../../../.github/workflows/sdk-auto-tag-release-commits.yaml)
will tag the head of that PR branch with a release tag, `sdk-release/v{NEW_VERSION}`.

Pushing the release tag triggers the [SDK Release workflow](../../../.github/workflows/sdk-release.yaml),
which will send a message to slack asking for release approval. Once approved, the workflow will
build the SDK wheel and upload it to PyPI. It will also build the docs and upload them to GCS.

### Manual Release

The [SDK Release workflow](../../../.github/workflows/sdk-release.yaml) also has a manual trigger.
Environment protection rules are set up such that it can only be run against a branch or tag with
prefix `sdk-release-*` or `sdk-release/*`.

Running it manually gives you the following options:
- check the `Publish to PyPI` box to publish the SDK to https://pypi.org/project/luminarycloud/
- check the `Upload docs to GCS` box to upload the SDK docs; jobmaster will pick
  these up and serve them at app.luminarycloud.com/docs/api/ after it's next reboot
- check the `Skip linting` box to skip the sanity checks that ensure the new release is documented
  and the version is bumped correctly. You probably don't want to skip linting unless the linter is
  making mistakes and you don't have time to fix it right this moment.

Notes:
- I've created an [sdk@luminarycloud.com
  group](https://groups.google.com/a/luminarycloud.com/g/sdk). This group will get
  PyPI related emails and if you need to "break glass" and access our project in
  PyPI, you can use this email to reset the password.
- In addition to the sdk@ email, Gavin and Prudhvi [are
maintainers](https://pypi.org/manage/project/luminarycloud/collaboration/) of
the package with our own accounts, and will use this for day to day managment.


## Manual Installation

There are two ways to run the SDK.
- If you just want to test it out or run unit tests, you can spin up a docker
  container as detailed in the [Quickstart section](#quickstart) above. This is
  the simplest way to get started with the SDK.
- Otherwise, you can continue with the instructions below. **If you aren't
  careful with your virtualenvs, there's a chance that you will mess up your
  dev environment, so I recommend the previous option.**

### Prerequisites
- [Install virtualenv](https://virtualenv.pypa.io/en/latest/installation.html")
- `luminarycloud-*.whl` file (either download a released SDK or [build the wheel
yourself](#building-the-wheel))

### (optional) Start a local apiserver

In separate/background shell:
```
> bazel run //go/core/cmd/apiserver:apiserver -- --insecure-apis
```

Please see the [apiserver README](/go/core/apiserver/README.md) for more details
on deployment options (e.g. using a local vs test0/main backend).

### Create a new virtualenv

**VS Code users:** it is recommended that you create the virtualenv via the
`Python: Create Environment` command instead of following the method below.

```sh
# create a new venv at a location of your choosing (e.g. ~/lc-sdk-venv),
# preferably OUTSIDE of the core repo so that git and gazelle don't pick
# up on its contents.
> virtualenv ~/lc-sdk-venv

# from here on, do everything in a venv
> source ~/lc-sdk-venv/bin/activate
```

**_NOTE_** - remember to `deactivate` the virtualenv after you're done with
the SDK or before running any of the other python-related scripts in this repository,
including `gazelle.py`, as well as any bazel rules that invoke python (such as the
`//gen:py_proto_library` rule), and even the `format.py` script which is part of the
git pre-commit hook.

If this sounds inconvenient, please take a look at the [Quickstart](#quickstart)
section at the top of the README.

### Install the python wheel

```sh
# --force-reinstall flag is only needed if you're reusing an old venv and want
# to replace any previously installed SDK
(lc-sdk-venv) > pip install --force-reinstall path/to/wheel/luminarycloud-*.whl

# use the REPL to import the SDK and make API calls
(lc-sdk-venv) > python
>>> import luminarycloud as lc
>>> lc.list_projects()

# run an example script that makes requests using the SDK
(lc-sdk-venv) > python my_script.py
```

You will probably also want to install the packages needed for the SDK with
```sh
pip install -r $CORE/python/sdk/requirements-dev.txt
```
The SDK tests also have some additional required packages that can be installed with
```sh
pip install -r $CORE/python/sdk_test/requirements.txt
```

## Building the wheel

### Prerequisites
- Install build: `pip install --upgrade build`

```sh
python -m build $CORE/python/sdk
```

You will find the resulting wheel file in `$CORE/python/sdk/dist`.

## Generating documentation

**[https://docs.eng.luminarycloud.com/python-sdk](https://docs.eng.luminarycloud.com/python-sdk)**

The docs are [automatically generated](../../../.github/workflows/generate-docs-site.yml)
and are hosted in our [internal documentation index](https://docs.eng.luminarycloud.com).

To generate the docs yourself:

```
docker compose run --build docs
```

To run the SDK quickstart notebook (which we make available on the doc website)

```
docker compose up --build quickstart
```

## Configuration

You may configure default values for the Luminary Python SDK using any of the
following environment variables.

| Name                | Default                                                    | Description                                                |
| ------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| LC_DOMAIN           | apis.luminarycloud.com                                     | The target API service domain.                             |
| LC_AUTH_DOMAIN      | luminarycloud-prod.us.auth0.com                            | The Auth0 tenant domain.                                   |
| LC_AUTH_CLIENT_ID   | JTsXa4fbArSCl6i9xylUpwrwpovtkss1                           | The Auth0 client ID for the SDK.                           |
| LC_AUTH_SERVICE_ID  | https://apis.luminarycloud.com                             | The Auth0 service identifier for the Luminary API service. |
| LC_REFRESH_ROTATION | TRUE                                                       | If TRUE, refresh token rotation is enabled.                |
| LC_CREDENTIALS_DIR  | ~/.config/luminarycloud or $APP_DATA/Roaming/luminarycloud | The directory to store credentials.                        |

To see the values for other Auth0 tenants, see:
`devops/terraform/ci-template/modules/auth0-metadata/main.tf`

### Using `.env`

You may set the above values inside a `.env` file placed at your project root or working directory.
The values set in a `.env` do not override existing environment variables.

## Development Guide

See [DEVELOPMENT.md](DEVELOPMENT.md) for more information on how to develop the SDK.
