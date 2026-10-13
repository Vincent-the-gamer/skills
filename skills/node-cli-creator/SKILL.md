---
name: node-cli-creator
description: Build a Node.js CLI in TypeScript — commands parsed with cac, code built with tsdown, deps updated with taze, source run with tsx. Use when the user wants to create, develop, or add features to a Node.js command-line tool or CLI project.
---

# Node CLI Creator

Build the Node.js CLI the user asks for, in TypeScript. The user almost always arrives with a feature request — "build me a CLI that does X" — not a request to scaffold an empty project. So the scaffold below is only the setup; the deliverable is the CLI itself: its commands, options, and behavior. Steps 0–8 stand the project up, Step 9 is the real work.

Stack:

| Concern            | Tool                                        |
| ------------------ | ------------------------------------------- |
| Command parsing    | [cac](https://github.com/cacjs/cac)         |
| Build / bundle     | [tsdown](https://tsdown.dev)                |
| Dependency updates | [taze](https://github.com/antfu/taze)       |
| Run from source    | [tsx](https://github.com/privatenumber/tsx) |

Work the steps in order. Below, `<pm>` is the chosen package manager.

## Step 0 — Understand the CLI to build

Turn the request into a concrete interface before writing code: the commands, each command's options and arguments, its input and output, and any files or APIs it touches. Infer what you can from the request and state those assumptions; ask the user only about gaps you genuinely cannot fill.

**Done when** you can list the commands with their options and describe what each one does.

## Step 1 — Pick the package manager

Detect which managers are installed (`npm`, `pnpm`, `yarn`, `bun`). If `npm` is the only one, use it and continue. If more than one is available, ask the user which to use.

**Done when** you know which manager every command will use.

## Step 2 — Decide how the CLI ships

Ask the user how the CLI reaches its users. The answer decides whether dependencies stay external or get bundled, and it drives the tsdown config in Step 6:

- **Publish to npm** — users run it via `npx <bin>`, a global install, or as a dependency. npm ships your `package.json` alongside the code, so everything under `dependencies` (including `cac`) is installed automatically. Keep dependencies **external** — this is tsdown's default, so no extra config is needed.
- **Local build only** — the built file is handed off on its own (copied elsewhere, run where `<pm> install` won't run). Nothing installs the dependencies, so the output must be **self-contained**: bundle every runtime dependency with `deps.alwaysBundle`.

**Done when** the distribution path is known.

## Step 3 — Initialize the project

Create the target directory if the user named a new one, then initialize a package:

```bash
<pm> init
```

Set `"type": "module"` in the generated `package.json`.

Create a `.gitignore` so resolved dependencies, build output, and OS junk stay out of version control:

```gitignore
node_modules
dist
.DS_Store
```

Add entries for anything else the project generates (env files, logs, caches).

**Done when** `package.json` exists with `"type": "module"`, and `.gitignore` ignores `node_modules`, `dist`, and `.DS_Store`.

## Step 4 — Install dependencies

`cac` is a **production** dependency: on the npm path npm installs it for consumers, and on the local-build path tsdown inlines it from `node_modules`:

```bash
<pm> add cac
```

The toolchain is all **devDependencies**:

```bash
<pm> add -D @types/node typescript tsdown taze tsx   # bun uses `bun add -d ...`
```

| Package       | Role                                     |
| ------------- | ---------------------------------------- |
| `cac`         | parse commands, options, and `--help`    |
| `@types/node` | Node.js types                            |
| `typescript`  | type checking                            |
| `tsdown`      | build and bundle                         |
| `taze`        | update dependencies                      |
| `tsx`         | run the CLI from source while developing |

**Done when** `cac` is under `dependencies` and the other five packages are under `devDependencies`.

## Step 5 — Configure taze

Create `taze.config.ts`:

```ts
import { defineConfig } from "taze";

export default defineConfig({
  write: true,
  install: true,
});
```

Add the update script to `package.json`:

Default command is `taze major`, if the user create a monorepo, install taze in root package and use `taze major -r`.

```json
{
  "scripts": {
    "dep": "taze major"
  }
}
```

**Done when** `taze.config.ts` exists and the `dep` script runs `taze major`.

## Step 6 — Configure TypeScript and tsdown

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

This is the whole config for the **publish to npm** path: tsdown externalizes everything under `dependencies` by default, and npm installs those for the user. On the **local build only** path, add `deps` so the runtime dependencies are inlined and the file runs without `node_modules`:

```ts
  deps: {
    alwaysBundle: ["cac"],
  },
```

Point `entry` at the real entry file if it is not `src/index.ts`.

**Done when** `tsconfig.json` and `tsdown.config.ts` exist and `entry` matches the file from Step 7.

## Step 7 — Write the entry point

Create `src/index.ts`. The shebang keeps the bundled file runnable:

```ts
#!/usr/bin/env node
import cac from "cac";

const cli = cac("<bin-name>");

cli
  .command("[input]", "Describe what the command does")
  .option("-e, --example", "An example flag")
  .action((input: string, options: { example?: boolean }) => {
    console.log(input || "hello from <bin-name>", options);
  });

cli.help();
cli.version("0.0.0");

cli.parse();
```

Then wire the CLI into `package.json`. `<bin-name>` is the command users type; the bundle path must match the file tsdown emits (default `dist/index.mjs`):

```json
{
  "bin": { "<bin-name>": "dist/index.mjs" },
  "files": ["dist"],
  "scripts": {
    "build": "tsdown",
    "dev": "tsx src/index.ts"
  }
}
```

The `files` array matters on the **publish to npm** path: npm falls back to `.gitignore` (which excludes `dist`) when choosing what to ship, so without it your bundle is left out of the package.

**Done when** `src/index.ts` parses at least one command, and `package.json` has a matching `bin` entry plus `build`/`dev` scripts.

## Step 8 — Verify the scaffold

The structure should match:

```
- src/
  | - index.ts
- .gitignore
- package.json
- taze.config.ts
- tsconfig.json
- tsdown.config.ts
```

Then confirm it builds and runs:

```bash
<pm> run build
node dist/index.mjs --help
```

**Done when** the build succeeds, the bundle exists in `dist/`, and `--help` prints the command's usage.

## Step 9 — Build the requested CLI

This is the point of the skill. Replace the placeholder command from Step 7 with the real commands from Step 0: implement their options and arguments, input and output, and the files or APIs they touch. Report errors with clear messages instead of letting them crash raw. On the local-build path, add each new runtime dependency to `deps.alwaysBundle` in `tsdown.config.ts`; add more entry files to `entry` if needed.

**Done when** the CLI performs every requested command, the build succeeds, and a smoke run of each command behaves as specified.
