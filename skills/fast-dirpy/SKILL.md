---
name: fast-dirpy
description: fast-dirpy is a Node.js CLI that extracts direct video links and downloads videos from supported sites. Use when the user says to use fast-dirpy to download a video or get a direct link.
license: Complete terms in LICENSE.txt
---

# fast-dirpy Usage Guide

Repo: https://github.com/Vincent-the-gamer/fast-dirpy

## Check the CLI

Run `fast-dirpy --version`.

- If a version prints: CLI is installed; invoke with `fast-dirpy <command>`.
- If the command is not found: ask the user which to use, then follow their choice:
  - Global install: `npm i fast-dirpy -g`, then `fast-dirpy <command>`.
  - No install: `npx fast-dirpy <command>`.

Do not choose the install method for the user.

## Rules

- **Visible terminal for downloads (preferred).** When downloading videos, prefer to explicitly open a *visible* terminal window and invoke the `fast-dirpy` CLI there, so the download progress is visible to the user. Do not run downloads in a hidden/background shell unless a visible window cannot be opened. On Windows, launch with `start`/`Start-Process` (e.g. `start "" cmd /k "fast-dirpy download --json-file params.json -H 127.0.0.1 -P 7890"` or `Start-Process wt -ArgumentList 'fast-dirpy','download','--json-file','params.json'`); on macOS/Linux use `open -a Terminal` / a new terminal emulator.
- Run fast-dirpy tasks in a visible terminal window.
- Follow this skill and the repo README. For exact flags run `fast-dirpy -h` or `fast-dirpy <command> -h`.
- Some supported sites need Google Chrome for Puppeteer. Supply `--chromePath <path>` or a config file with `puppeteer.executablePath`.

## Supported sites

YouTube, Bilibili, and `.m3u8` videos. NSFW (under `<details>` in README): Animehentai, Koreanpornmovies, XVideos, Hanime1.me, wow.xxx, rule34.xyz, lewd ninja, sfmcompile.club, ugoira (pixiv GIF), missav, xhamster.

## Config file (optional)

`fast-dirpy.config.[ts, mts, cts, js, mjs, cjs, json]` in the working directory, or pass `-c <path>`.

```ts
import { defineConfig } from 'fast-dirpy'

export default defineConfig({
  proxy: { protocol: 'http', host: '127.0.0.1', port: 7890 },
  timeout: 20000,
  puppeteer: {
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  },
})
```

## Commands

### Get a direct link

```shell
fast-dirpy get <url> [-H <host>] [-P <port>] [-c <config>] [--silent] [--chromePath <path>]
```

Example: `fast-dirpy get https://www.bilibili.com/video/BV1TSPeeGE35`

### Download a video

```shell
fast-dirpy download (--json '<json>' | --json-file <path>) [-H <host>] [-P <port>] [-c <config>] [--silent] [--chromePath <path>]
```

- `--json` / `-j`: JSON array of `{ "url": "...", "path": "./out.mp4" }`.
- `--json-file` / `-F`: path to a JSON file with the same array. Parallel download supported (v1.0.0+).
- `path` is the output file.

Examples:

```shell
fast-dirpy download --json '[{"url":"https://www.bilibili.com/video/BV1uEAWzuEHC","path":"./cmd-test.mp4"}]'
fast-dirpy download --json-file ./params.json
```

### Download a Pixiv GIF (ugoira)

```shell
fast-dirpy ugoira <artwork_url> [-H <host>] [-P <port>] [--silent]
```

## Special cases

- **missav / xhamster**: these have Cloudflare challenges. Manually download the HTML page (no JS/CSS, HTML only), then pass the local file with a scheme prefix:
  - `fast-dirpy download --json '[{"url":"missav:/path/to/xxx.html","path":"./msav-test.mp4"}]'`
  - `fast-dirpy download --json '[{"url":"xhamster:/path/to/xxx.html","path":"./xh-test.mp4"}]'`
  - missav method is unstable and may return HTTP 429.
- **Proxy**: pass `-H`/`-P`, or omit when configured in the config file.
- **params.json**: array of `{ "url", "path" }` (optional `cwd` for an external config). Do not read it; pass it via `--json-file`.