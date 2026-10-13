#!/usr/bin/env node
// Regenerates src/api/schema.d.ts from the running API.
//
// The default lives here instead of in the package.json script because bun's shell does not
// expand ${VITE_API_URL:-http://localhost:8000}; that POSIX syntax silently passes through as a
// literal filename on Windows. Node reads the environment the same way on Windows, Linux and macOS.
//
// Usage: bun run gen:api            -> http://localhost:8000
//        VITE_API_URL=https://x bun run gen:api

import { spawnSync } from 'node:child_process'

const apiUrl = process.env.VITE_API_URL ?? 'http://localhost:8000'
const isWindows = process.platform === 'win32'
const bin = isWindows ? 'openapi-typescript.exe' : 'openapi-typescript'

const result = spawnSync(bin, [`${apiUrl}/openapi.json`, '-o', 'src/api/schema.d.ts'], {
  stdio: 'inherit',
  shell: isWindows,
})

if (result.error) {
  console.error(`gen:api failed to start openapi-typescript: ${result.error.message}`)
  process.exit(1)
}

process.exit(result.status ?? 1)
