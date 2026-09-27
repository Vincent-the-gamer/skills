import { defineConfig } from 'tsdown'

export default defineConfig({
  entry: [
    './src/jev.ts',
  ],
  clean: true,
  format: ['esm'],
  dts: true,
  minify: true,
  // compatible with __dirname in cjs and import.meta.url in mjs.
  shims: true,
  deps: {
    alwaysBundle: ["axios"]
  }
})