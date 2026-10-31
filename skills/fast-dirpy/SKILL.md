---
name: fast-dirpy
version: 1.0.2
description: fast-dirpy is a CLI based on Node.js, it can extract direct links and download videos from video websites. Use when the user says using fast-dirpy to download videos.
license: Complete terms in LICENSE.txt
---

# fast-dirpy Usage Guide

[GitHub Repository](https://github.com/Vincent-the-gamer/fast-dirpy)

## Check if the CLI exists.

Check if fast-dirpy exists: `fast-dirpy --version`

If not, you can call fast-dirpy CLI in two ways:

- Global install: `npm i fast-dirpy -g`, then `fast-dirpy <command>`
- No installation, directly use it through npx: `npx fast-dirpy <command>`

## CLI Usage

```bash
fast-dirpy -h
```

## Rules

- You must open a visible terminal window and run the fast-dirpy tasks.
- Follow the repo's README to use the CLI.

## Configuration

You can configure fast-dirpy by creating a fast-dirpy.config.(js, ts, mjs, mts, json), see GitHub Repo for more info.

**Important**: The config file should in your current working directory, or else giving a config file path:

```bash
fast-dirpy -c fast-dirpy.config.json download ...
```

Example:

```ts
import { defineConfig } from "./fast-dirpy";

export default defineConfig({
  proxy: {
    protocol: "http",
    host: "127.0.0.1",
    port: 7890,
  },
  timeout: 20000, // 20s
  puppeteer: {
    executablePath:
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless: true,
  },
});
```
