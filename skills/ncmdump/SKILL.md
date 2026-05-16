---
name: ncmdump
version: 1.0.1
description: ncmdump is a tool to dump the .ncm file into .mp3/.flac format. Use when the user say decode .ncm file into .mp3/.flac format, or use ncmdump.
license: Complete terms in LICENSE.txt
---

# Guide

The [ncmdump.rs](https://github.com/iqiziqi/ncmdump.rs) GitHub repo provides a tool to dump the .ncm file.

## Check Installation

Firstly, check ncmdump:

```bash
ncmdump --version
```

If it says ncmdump not found, then check if Rust is installed:

```bash
cargo --version
```

If Rust is installed, using Cargo to install ncmdump:

```bash
cargo install ncmdump-bin
```

If it says cargo not found, download ncmdump from **github releases**, use latest version:

[ncmdump.rs latest release](https://github.com/iqiziqi/ncmdump.rs/releases/latest)

Ensure you choose the right operating system and architecture.

**If you can’t find the binary file, try GitHub Release API.**

## Usage

> [!IMPORTANT]
> If you download ncmdump from release, ensure you execute it in the directory you stored the binary file.

```bash
Usage: ncmdump [OPTIONS] [FILES]...

Arguments:
  [FILES]...  Specified the files to convert

Options:
  -o, --output <OUTPUT>  Specified the output directory. Default it's the same directory with input file
  -v, --verbose          Verbosely list files processing
  -h, --help             Print help
  -V, --version          Print version
```

Example:

```bash
ncmdump -o ./123.mp3 aa.ncm
```

## Avoid the issue

Currently, ncmdump can't handle the .ncm file which name includes "[" and "]", so if you meet these files, remove the "[" and "]"

For detail, see [Issue #24](https://github.com/iqiziqi/ncmdump.rs/issues/24)
