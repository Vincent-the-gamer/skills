---
name: fast-dirpy
version: 1.0.1
description: fast-dirpy is a CLI based on Node.js, it can extract direct links and download videos from video websites.
license: Complete terms in LICENSE.txt
---

# fast-dirpy Usage Guide

[GitHub Repository](https://github.com/Vincent-the-gamer/fast-dirpy)

You can call fast-dirpy CLI in two ways:

- Global install: `npm i fast-dirpy -g`, then `fast-dirpy <command>`
- No installation, directly use it through npx: `npx fast-dirpy <command>`

Get further help with: `fast-dirpy --help`

## Rules

1. Before run commands, run `fast-dirpy -v` to check if fast-dirpy is installed, if not, use npx.
2. Run the task in the background asynchronously, don't block the Agent, and tell user the PID of process.
3. After doing rule 2, generate the `.log` file in the same path of video you download, then write the log content into it.
4. If commands fails, show the user error message and stop running.
5. When task is complete, tell user the result, no matter success or failure.
6. If network request timed out, show the user error message and stop running.

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

## Get Direct Link

```bash
fast-dirpy get <url>
```

## Download Video

**JSON Params**:

```bash
fast-dirpy download --json '[{"url": "xxx", "path": "./test.mp4"}]'
```

**JSON File Params**:

```bash
fast-dirpy download --jsonFile ./params.json
```
