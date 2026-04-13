import { defineConfig } from 'tsdown'

export default defineConfig({
  entry: [
    "./src/{index,cli}.ts"
  ],
  clean: true,
  format: ["esm", "cjs"],
  dts: true,
  minify: true,
  // compatible with __dirname in cjs and import.meta.url in mjs.
  shims: true
})