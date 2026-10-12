# node-cli-creator

A skill to build a Node.js CLI package in TypeScript with [cac](https://github.com/cacjs/cac).

It is **not just a scaffolder**. You normally reach for it when you have a feature request — "build me a CLI that does X" — so the skill stands up the project and then implements the commands you asked for. Scaffolding is the setup; the CLI itself is the deliverable.

## Stack

| Concern            | Tool                                        |
| ------------------ | ------------------------------------------- |
| Command parsing    | [cac](https://github.com/cacjs/cac)         |
| Build / bundle     | [tsdown](https://tsdown.dev)                |
| Dependency updates | [taze](https://github.com/antfu/taze)       |
| Run from source    | [tsx](https://github.com/privatenumber/tsx) |

## Steps

### Step 0: Understand the CLI to build

Turn the request into a concrete interface first: the commands, their options and arguments, input/output, and any files or APIs they touch. Infer what you can and state assumptions; ask the user only about real gaps.

### Step 1: Ask the user for package manager

Ask the user first if multiple package managers are installed (npm, pnpm, yarn, bun). If only `npm` is present, skip this step.

### Step 2: Decide how the CLI ships

Ask the user how the CLI reaches its users. The answer decides whether dependencies stay external or get bundled:

- **Publish to npm** — users run it via `npx`, a global install, or as a dependency. npm ships `package.json` alongside the code, so everything under `dependencies` (including `cac`) is installed automatically. Keep dependencies external (tsdown's default), so no bundling is needed.
- **Local build only** — the built file is handed off on its own, where nothing runs an install. Bundle the runtime dependencies with `deps.alwaysBundle` so the output is self-contained.

### Step 3: Initialize Node project

Use the chosen package manager.

```bash
# pnpm/bun...
npm init
```

Set `"type": "module"` in `package.json`, then create a `.gitignore`:

```gitignore
node_modules
dist
.DS_Store
```

Add entries for anything else the project generates (env files, logs, caches).

### Step 4: Install dependencies

Require [cac](https://github.com/cacjs/cac) as a production dependency, then add the following as `devDependencies`:

- `@types/node`
- `typescript`
- `tsdown` — to build the package.
- `taze` — make the deps easy to update.
- `tsx` — for users to execute the cli for test

`cac` is a production dependency in both shipping paths: npm installs it for consumers on the npm path, and tsdown inlines it from `node_modules` on the local-build path.

### Step 5: taze.config.ts

Create a `taze.config.ts` file in the project root.

```ts
import { defineConfig } from "taze";

export default defineConfig({
  write: true,
  install: true,
});
```

Then add the script to `package.json`:

```json
{
  "scripts": {
    "dep": "taze major -I"
  }
}
```

### Step 6: tsconfig.json and tsdown.config.ts

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["ESNext"],
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "strict": true,
    "strictNullChecks": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipDefaultLibCheck": true,
    "skipLibCheck": true
  }
}
```

Create `tsdown.config.ts`:

```ts
import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["src/index.ts"],
  clean: true,
  format: ["esm"],
  dts: true,
  minify: true,
  // compatible with __dirname in cjs and import.meta.url in mjs.
  shims: true,
});
```

This is the whole config for the **publish to npm** path: tsdown externalizes `dependencies` by default, and npm installs them for the user. On the **local build only** path, add `deps` to inline the runtime dependencies so the single output file runs without `node_modules`:

```ts
  deps: {
    alwaysBundle: ["cac"],
  },
```

### Step 7: Write the entry point

Create `src/index.ts` (the shebang keeps the bundled file runnable), and wire `bin` plus the `build`/`dev` scripts into `package.json`. On the npm path, also add a `files` field listing `dist` — npm falls back to `.gitignore` (which excludes `dist`), so without it the bundle is left out of the published package.

### Step 8: Check project hierarchy

```
- src
  | - index.ts
- .gitignore
- package.json
- taze.config.ts
- tsconfig.json
- tsdown.config.ts
```

Then verify it builds and runs:

```bash
<pm> run build
node dist/index.mjs --help
```

### Step 9: Build the requested CLI

Implement the user's actual feature: their commands, options, and behavior — not just the scaffold. On the local-build path, add each new runtime dependency to `alwaysBundle` in `tsdown.config.ts`, and add entry files to `entry` if needed.
