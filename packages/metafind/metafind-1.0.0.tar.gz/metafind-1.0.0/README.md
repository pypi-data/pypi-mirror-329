# Metafind

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fsapph2c%2Fmetafind%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoSize=auto)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sapph2c/metafind/ci.yml?style=for-the-badge&logo=github&logoSize=auto)
![GitHub deployments](https://img.shields.io/github/deployments/sapph2c/metafind/pypi?style=for-the-badge&logo=pypi&logoColor=white&logoSize=auto)

**Metafind** is a metadata analysis tool written for CSEC-473 - Penetration Testing.

## Features

- Ability to retrieve and scrub file metadata.
- Lists unique discovered metadata tags.

## Install

Metafind is available as a Python package on PyPI and can be installed using `uv` (recommended), `pipx`, or `pip`.

**Note**: python 3.13+ is required

Install using uv:

```bash
uv install tool metafind@latest
```

Install using pipx:

```bash
pipx install metafind
```

Install using pip:

```bash
pip install metafind
```

## Usage

> [!IMPORTANT]  
> Metafind requires a metadata backend to be available within your system path.
>
> This can be specified in the CLI via `--backend`, which defaults to `exiftool`.
>
> For a full list of supported backends, see [Supported Backends](#Supported-Backends)

CLI options:

```bash
> metafind --help

Usage: metafind [OPTIONS] COMMAND [ARGS]...

  Metadata analysis tool created for CSEC-473 - Penetration Testing.

  Authored by sapph2c

Options:
  --help  Show this message and exit.

Commands:
  fetch   get file(s) metadata
  scrub   scrub file(s) metadata
  unique  get unique tags from file(s)
```

Retrieving file metadata:

```bash
metafind fetch <path-to-file>
```

Scrubbing metadata: (It's recommended to make a backup of the specified file(s), as this operation is non-reversible)

```bash
metafind scrub <path-to-file>
```

Listing all unique metadata tags:

```bash
metafind unique <path-to-file>
```

## Supported Backends

- [Exiftool](https://exiftool.org)

