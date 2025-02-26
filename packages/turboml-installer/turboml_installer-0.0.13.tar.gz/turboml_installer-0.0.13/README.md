# TurboML Installer

A conda/pixi-based installer for the [TurboML SDK](https://pypi.org/project/turboml-sdk/). Currently, the installer supports x86_64 Linux.

## Prerequisites

- An active [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Pixi](https://pixi.sh/latest/) environment.
  - With Python 3.11 (our SDK is constrained to Python 3.11).

On Google colab, these prerequisites are already met as of Jan 2025.

## Installation

`pip install turboml-installer` / `uv pip install turboml-installer`

## Usage

```python
import turboml_installer ; turboml_installer.install()
```
