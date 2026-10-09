---
name: novnc
description: Deploy noVNC — a browser VNC client — using websockify-js. Use when the user wants to view or control a VNC server in the browser, or to set up noVNC + websockify.
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

If `websockify-js/websockify` already exists with a `noVNC/` folder and installed `node_modules`, the setup is in place — skip to step 3.

Otherwise, get the websockify folder and clone noVNC into it:

```bash
git clone --depth 1 https://github.com/novnc/websockify-js.git
git clone --depth 1 https://github.com/novnc/noVNC.git websockify-js/websockify/noVNC
```

Install dependencies:

```bash
cd websockify-js/websockify && npm install
```

Expected layout:

```
websockify-js/websockify
  - package.json
  - websockify.js
  - noVNC/          # contains vnc.html
```

Configured websockify opens the noVNC entry point `vnc.html`; confirm it:

```bash
grep -n "vnc.html" websockify-js/websockify/websockify.js
```

Done when the layout matches, dependencies are installed, and websockify serves `vnc.html`.

## 3. Start the bridge

Run from the websockify folder, passing `<web-port>` then `<target>`:

```bash
cd websockify-js/websockify && node websockify.js --web noVNC --target-option allowLoopback=yes <web-port> <target>
```

Example — VNC server on `localhost:5900` served on web port `9000`:

```bash
cd websockify-js/websockify && node websockify.js --web noVNC --target-option allowLoopback=yes 9000 localhost:5900
```

`--target-option allowLoopback=yes` permits a `localhost` target, which websockify blocks by default.

Start it in the background and report the PID. Done when the browser opens `http://localhost:<web-port>` — that root URL is the noVNC page — and connects to the **target**.
