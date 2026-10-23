# noVNC

## Check local VNC service

Check if vnc service is exist, and its' port.

## How to deploy

We use Node.js + [websockify-js](https://github.com/novnc/websockify-js).

Before downloading, check whether `websockify-js` and a noVNC folder already exist on the machine and reuse them. Clone only what is missing.

First:

Download: https://github.com/novnc/websockify-js/tree/master/websockify folder.

Hierarchy:

```
novnc/websockify-js
  ...
  - websockify
    | - package.json
    | - websockify.js
 ...
```

Second:

Clone: [noVNC](https://github.com/novnc/noVNC) into websockify folder. Ask first whether GBK clipboard support is needed; if yes, clone [noVNC-GBK-Clipboard](https://github.com/Vincent-the-gamer/noVNC-GBK-Clipboard) there instead:

```
novnc/websockify-js
  ...
  - websockify
    | - package.json
    | - websockify.js
    | - noVNC
 ...
```

and check `websockify.js`, ensure it opens `vnc.html` in noVNC folder, not other name.

Third:

Install dependencies

```bash
# yarn i, pnpm i...
npm i
```

then using:

```bash
# <port> is vnc service port
node websockify.js --web noVNC --target-option allowLoopback=yes 9000 localhost:<port>
```

to start.
