---
name: fast-dirpy
description: fast-dirpy is a CLI based on Node.js, it can extract direct links and download videos from video websites.
license: Complete terms in LICENSE.txt
---

# fast-dirpy Usage Guide

[GitHub Repository](https://github.com/Vincent-the-gamer/fast-dirpy)

You can call fast-dirpy CLI in two ways:

- Global install: `npm i fast-dirpy -g`, then `fast-dirpy <command>`
- No installation, directly use it through npx: `npx fast-dirpy <command>`

Get further help with: `fast-dirpy --help`

## Configuration

You can configure fast-dirpy by creating a fast-dirpy.config.(js, ts, json), see GitHub Repo for more info.

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
