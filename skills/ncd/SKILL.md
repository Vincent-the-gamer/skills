---
name: ncd
description: ncd (ncm dumper) is a CLI for batch-converting .ncm files to .mp3. Use when the user says using ncd to convert .ncm files.
license: Complete terms in LICENSE.txt
---

# ncd Usage Guide

[GitHub Repository](https://github.com/Vincent-the-gamer/ncd)

ncd is a Rust CLI that batch-converts `.ncm` (NetEase Cloud Music encrypted) files in a directory to `.mp3`.

## Check Installation

Check if ncd is installed:

```bash
ncd --version
```

If not found, download the binary from GitHub Releases, use latest version:

[ncd latest release](https://github.com/Vincent-the-gamer/ncd/releases/latest)

Ensure you choose the right operating system and architecture.

**If you can't find the binary file, try GitHub Release API.**

After downloading, make it available in `PATH`:

**macOS / Linux:**

```bash
chmod +x ncd-*
sudo mv ncd-* /usr/local/bin/ncd
```

**Windows:**

1. Rename the downloaded `.exe` to `ncd.exe`
2. Add its directory to the system `PATH` environment variable

## Usage

```bash
ncd <SRC_DIR> [OUT_DIR]
```

- `SRC_DIR`: directory containing `.ncm` files (required)
- `OUT_DIR`: output directory for `.mp3` files (optional, defaults to `<cwd>/output`)

Each `.ncm` file in `SRC_DIR` is converted to `<filename>.mp3` in `OUT_DIR`.

> [!CAUTION]
> ncd will **delete non-`.ncm` files** from `SRC_DIR`. Put only `.ncm` files in the source directory, or use a dedicated directory.

## Example

```bash
ncd ./ncm_files ./mp3_output
```
