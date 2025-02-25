# mopidy-debugrel

![PyPI - Version](https://img.shields.io/pypi/v/mopidy-debugrel?link=https://pypi.org/p/mopidy-debugrel)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sapristi/mopidy-debugrel/ci.yml?link=https://github.com/sapristi/mopidy-debugrel/actions/workflows/ci.yml)
![Codecov](https://img.shields.io/codecov/c/gh/sapristi/mopidy-debugrel?link=https://codecov.io/gh/sapristi/mopidy-debugrel)

Mopidy extension that provides a Read-Eval loop over http, for debugging purpose.

**Warning**: enabling this extension leaves your server vulnerable, make sure mopidy is not exposed to the web when enabling it, and disable it when you are done.


## Installation

Install by running:

```sh
python3 -m pip install mopidy-debugrel
```

See https://mopidy.com/ext/debugrel/ for alternative installation methods.


## Configuration

This extension is disabled by default. To enable it, add the following to your mopidy configuration file:

```ini
[debugrel]
enabled = true
# Adapt enabled_until to your needs
enabled_until = 2025-05-01
```

## Usage

### Overview

This extension exposes a single API endpoint, that will execute the python code that you pass in your request. For example:

```python
import requests

MOPIDY_HOST = "localhost"
MOPIDY_PORT = "6680"

code = """
logger.info("hello")
"""

requests.post(f"http://{MOPIDY_HOST}:{MOPIDY_PORT}/debugrel/debug", json={"source": code})
```

Running this trigger the execution of `code` in mopidy, resulting in the following logs:
```
mopidy[1771]: INFO     2025-02-23 14:39:29,689 [1771:HttpServer] mopidy_debugrel
mopidy[1771]:   hello
```

In the context of execution, you can access mopidy config with `self.config`, and mopidy core with `self.core`

### Examples

Some examples of code that you can use.

1. Access the backends

  ```python
  code = """
  logger.info(self.core.backends.get())
  """

  requests.post(f"http://{MOPIDY_HOST}:{MOPIDY_PORT}/debugrel/debug", json={"source": code})
  ```

  Logs:
  ```
  mopidy[1771]: INFO     2025-02-23 14:55:59,966 [1771:HttpServer] mopidy_debugrel
  mopidy[1771]:   [<ActorProxy for FileBackend (urn:uuid:55234968-8840-4618-8bdb-f990c084fcac), attr_path=()>, <ActorProxy for M3UBackend (urn:uuid:eb60e9fe-5db9-4d8f-8444-d586aaae8573), attr_path=()>, <ActorProxy for StreamBackend (urn:uuid:1050cc10-6178-4820-aaf8-d4ab14cec939), attr_path=()>, <ActorProxy for BookmarksBackend (urn:uuid:ade7e4bd-2130-421e-9c98-aadeeaa77863), attr_path=()>, <ActorProxy for TidalBackend (urn:uuid:6cbdb63d-b5a5-4bc5-8ceb-7511457ac98a), attr_path=()>]
  ```


2. Instantiate a tidal backend

 ```python
  code = """
  from mopidy_tidal.backend import TidalBackend
  backend = TidalBackend(self.config, None)
  logger.info(backend)
  """

  requests.post("http://gidouille.local:6680/debugrel/debug", json={"source": code})  ```
  ```

  Logs:
  ```
  mopidy[1771]: INFO     2025-02-23 14:54:53,030 [1771:HttpServer] mopidy_debugrel
  mopidy[1771]:   TidalBackend (urn:uuid:b496ce6c-d856-4e37-939f-f311d067892d)
  ```

3. Print config entries:
 ```python
  code = """
  for key, value in self.config.items():
      logger.info(f"{key}: {value}")
  """

  requests.post("http://gidouille.local:6680/debugrel/debug", json={"source": code})  ```
  ```

## Project resources

- [Source code](https://github.com/sapristi/mopidy-debugrel)
- [Issues](https://github.com/sapristi/mopidy-debugrel/issues)
- [Releases](https://github.com/sapristi/mopidy-debugrel/releases)


## Development

### Set up development environment

Clone the repo using, e.g. using [gh](https://cli.github.com/):

```sh
gh repo clone sapristi/mopidy-debugrel
```

Enter the directory, and install dependencies using [uv](https://docs.astral.sh/uv/):

```sh
cd mopidy-debugrel/
uv sync
```

### Making a release

To make a release to PyPI, go to the project's [GitHub releases
page](https://github.com/sapristi/mopidy-debugrel/releases)
and click the "Draft a new release" button.

In the "choose a tag" dropdown, select the tag you want to release or create a
new tag, e.g. `v0.1.0`. Add a title, e.g. `v0.1.0`, and a description of the changes.

Decide if the release is a pre-release (alpha, beta, or release candidate) or
should be marked as the latest release, and click "Publish release".

Once the releease is created, the `release.yml` GitHub Action will automatically
build and publish the release to
[PyPI](https://pypi.org/project/mopidy-debugrel/).


## Credits

- Original author: [Mathias Millet](https://github.com/sapristi)
- Current maintainer: [Mathias Millet](https://github.com/sapristi)
- [Contributors](https://github.com/sapristi/mopidy-debugrel/graphs/contributors)
