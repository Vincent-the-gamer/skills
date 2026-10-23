---
name: novnc
description: Deploy noVNC — a browser VNC client — using websockify-js. Use when the user wants to view or control a VNC server in the browser, to set up noVNC + websockify, or needs GBK clipboard support in noVNC.
license: Complete terms in LICENSE.txt
---

# noVNC Usage Guide

[noVNC](https://github.com/novnc/noVNC) is a browser VNC client. A browser can't speak raw VNC, so [websockify-js](https://github.com/novnc/websockify-js) bridges a WebSocket port to a raw VNC **target**.

Two ports matter:

- **web port** — where the browser loads noVNC (e.g. `9000`)
- **target** — the VNC server as `host:port` (e.g. `localhost:5900`)

Requires Node.js + npm.

## 1. Find the VNC service

List listening ports and locate the VNC one (commonly `5900`+display):

```bash
lsof -iTCP -sTCP:LISTEN -P -n | grep -i vnc
```

If that finds nothing, probe the common range `5900`–`5910`.

Done when you have a live `host:port` **target** to bridge to.

## 2. Set up websockify

Reuse what is already on the machine and clone only what is missing. Look in the working directory and, shallowly, under the home folder:

```bash
ls -d websockify-js noVNC 2>/dev/null
find ~ -maxdepth 4 -type d \( -name websockify-js -o -name noVNC \) 2>/dev/null
```

A usable websockify has `websockify/websockify.js`; a usable noVNC contains `vnc.html`. Run these commands from the folder holding the existing `websockify-js`, or the parent where it will be cloned.

Keep a noVNC that is already present. `git -C /path/to/noVNC remote get-url origin` tells the flavors apart: a URL containing `noVNC-GBK-Clipboard` is the GBK fork, `novnc/noVNC` is the official project.

Fetch a websockify only if none is usable:

```bash
git clone --depth 1 https://github.com/novnc/websockify-js.git
```

When the noVNC you keep lives outside the websockify folder and `websockify-js/websockify/noVNC` is still empty, link it into place instead of cloning:

```bash
ln -s /absolute/path/to/noVNC websockify-js/websockify/noVNC
```

When noVNC must be fetched — nothing usable found, or the user asks for GBK support the existing copy lacks — ask the user one question:

> Do you need GBK clipboard support?

Then run exactly one clone, based on the answer:

```bash
# Official noVNC
git clone --depth 1 https://github.com/novnc/noVNC.git websockify-js/websockify/noVNC

# GBK clipboard fork — instead of the official clone
# when the user answered yes
git clone --depth 1 https://github.com/Vincent-the-gamer/noVNC-GBK-Clipboard.git websockify-js/websockify/noVNC
```

Replacing an existing official copy needs the user's confirmation first.

Install dependencies if `node_modules` is missing:

```bash
cd websockify-js/websockify && npm install
```

Expected layout:

```
websockify-js/websockify
  - package.json
  - websockify.js
  - node_modules/
  - noVNC/          # contains vnc.html; may be a symlink to an existing copy
```

Configured websockify opens the noVNC entry point `vnc.html`; confirm it:

```bash
grep -n "vnc.html" websockify-js/websockify/websockify.js
```

Done when a websockify folder with installed dependencies serves a noVNC containing `vnc.html`, whether reused or freshly cloned.

## 3. Start the bridge

Run from the websockify folder set up in step 2, passing `<web-port>` then `<target>` (the example assumes it is `websockify-js/websockify`):

```bash
cd websockify-js/websockify && node websockify.js --web noVNC --target-option allowLoopback=yes <web-port> <target>
```

Example — VNC server on `localhost:5900` served on web port `9000`:

```bash
cd websockify-js/websockify && node websockify.js --web noVNC --target-option allowLoopback=yes 9000 localhost:5900
```

`--target-option allowLoopback=yes` permits a `localhost` target, which websockify blocks by default.

Start it in the background and report the PID. Done when the browser opens `http://localhost:<web-port>` — that root URL is the noVNC page — and connects to the **target**.
